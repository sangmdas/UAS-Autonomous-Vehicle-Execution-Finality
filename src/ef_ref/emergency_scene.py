from __future__ import annotations

from dataclasses import dataclass

from .crypto import canonical_bytes, domain_hash


@dataclass(frozen=True)
class SceneEvidence:
    channel_id: str
    physical_source_id: str
    valid: bool


@dataclass(frozen=True)
class EmergencyAuthority:
    vehicle_id: str
    incident_id: str
    scene_polygon: tuple[tuple[float, float], ...]
    exception_classes: tuple[str, ...]
    expiry_ms: int
    policy_epoch: int
    revocation_epoch: int
    nonce: str
    q_required: int
    scene_epoch: int


def scene_commitment(authority: EmergencyAuthority, evidence_digest: bytes, temporary_control_digest: bytes) -> bytes:
    obj = {
        "incident_id": authority.incident_id,
        "scene_polygon": authority.scene_polygon,
        "evidence_digest": evidence_digest.hex(),
        "temporary_control_digest": temporary_control_digest.hex(),
        "scene_epoch": authority.scene_epoch,
    }
    return domain_hash("EMERGENCY-SCENE", canonical_bytes(obj))


def corroborated(evidence: list[SceneEvidence], q_required: int) -> bool:
    # Multiple channels from the same physical source count only once.
    unique_valid = {e.physical_source_id for e in evidence if e.valid}
    return len(unique_valid) >= q_required


def point_in_dilated_bbox(point: tuple[float, float], polygon: tuple[tuple[float, float], ...], delta: float) -> bool:
    xs = [p[0] for p in polygon]
    ys = [p[1] for p in polygon]
    return min(xs) - delta <= point[0] <= max(xs) + delta and min(ys) - delta <= point[1] <= max(ys) + delta


def allow_emergency(*, authority: EmergencyAuthority, vehicle_id: str, exception_class: str, position: tuple[float, float], evidence: list[SceneEvidence], now_ms: int, current_policy_epoch: int, current_revocation_epoch: int, delta_loc: float, hard_safety_ok: bool, consumed: bool, revoked: bool) -> bool:
    e_t = (
        vehicle_id == authority.vehicle_id
        and now_ms <= authority.expiry_ms
        and not revoked
        and not consumed
        and current_policy_epoch == authority.policy_epoch
        and current_revocation_epoch == authority.revocation_epoch
        and corroborated(evidence, authority.q_required)
        and point_in_dilated_bbox(position, authority.scene_polygon, delta_loc)
    )
    return e_t and exception_class in authority.exception_classes and hard_safety_ok
