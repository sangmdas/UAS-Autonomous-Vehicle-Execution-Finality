from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any


@dataclass(frozen=True)
class CandidateAct:
    device_id: str
    act_id: str
    act_class: str
    sink_id: str
    params: dict[str, Any]
    authority_ref: str
    policy_epoch: int
    revocation_epoch: int
    context: dict[str, Any]
    nonce: str
    expiry_ms: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class AuthorityState:
    authority_ref: str
    allowed_classes: tuple[str, ...]
    device_id: str
    sink_ids: tuple[str, ...]
    min_policy_epoch: int
    min_revocation_epoch: int
    expiry_ms: int
    envelope: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class BPC:
    device_id: str
    act_class: str
    sink_id: str
    authority_ref: str
    policy_epoch: int
    revocation_epoch: int
    freshness: str
    expiry_ms: int
    act_digest: bytes
    context_digest: bytes
    binding_trunc: bytes
    tag: bytes


@dataclass(frozen=True)
class Receipt:
    counter: int
    decision: str
    act_digest: bytes
    binding: bytes
    sink_id: str
    context_digest: bytes
    nonce: str
    previous_digest: bytes
    reason: str = ""


@dataclass(frozen=True)
class Fragment:
    session_id: str
    root: bytes
    index: int
    total: int
    payload: bytes
    auth: bytes


@dataclass(frozen=True)
class AER:
    device_id: str
    epoch_id: str
    interval: int
    act_class: str
    decision: str
    sink_class: str
    receipt_counter: int
    header: bytes
    tag: bytes


@dataclass(frozen=True)
class KDR:
    epoch_id: str
    evidence_interval: int
    key_index: int
    key: bytes


@dataclass(frozen=True)
class Track:
    track_ref: str
    source_class: str
    position_xy: tuple[float, float]
    velocity_xy: tuple[float, float]
    uncertainty_m: float
    freshness_ms: int
    encounter_class: str = "generic"


@dataclass(frozen=True)
class Maneuver:
    maneuver_id: str
    velocity_xy: tuple[float, float]
    resolution_epoch: int
    conflict_root: bytes
    sink_id: str


@dataclass
class ControlState:
    sink_id: str
    current_controller: str
    current_epoch: int
    current_envelope: dict[str, Any]
    pending_controller: str | None = None
    pending_epoch: int | None = None
    safe_only: bool = False
