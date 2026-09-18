from __future__ import annotations

import pytest

from ef_ref.models import CandidateAct, AuthorityState


@pytest.fixture
def root_key() -> bytes:
    return bytes.fromhex("11" * 32)


@pytest.fixture
def sink_key() -> bytes:
    return bytes.fromhex("22" * 32)


@pytest.fixture
def session_nonce() -> str:
    return "session-2026-09-18-A"


@pytest.fixture
def baseline_act() -> CandidateAct:
    return CandidateAct(
        device_id="uas:TEST-001",
        act_id="act-0001",
        act_class="PAYLOAD_RELEASE",
        sink_id="payload-latch-1",
        params={"drop_zone":"DZ-7", "altitude_m":12.0, "speed_mps":2.0},
        authority_ref="AUTH-7",
        policy_epoch=7,
        revocation_epoch=9,
        context={"geofence":"G12", "mission_phase":"DELIVERY", "payload_locked":True},
        nonce="nonce-0001",
        expiry_ms=2_000_000,
    )


@pytest.fixture
def authority() -> AuthorityState:
    return AuthorityState(
        authority_ref="AUTH-7",
        allowed_classes=("PAYLOAD_RELEASE", "KINETIC_ENVELOPE"),
        device_id="uas:TEST-001",
        sink_ids=("payload-latch-1", "motion-sink-1"),
        min_policy_epoch=7,
        min_revocation_epoch=9,
        expiry_ms=2_000_000,
        envelope={"altitude_m_max":20.0},
    )
