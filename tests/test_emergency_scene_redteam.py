from ef_ref.emergency_scene import EmergencyAuthority, SceneEvidence, corroborated, allow_emergency


def authority():
    return EmergencyAuthority(
        vehicle_id="AV-1",
        incident_id="INC-77",
        scene_polygon=((0,0),(10,0),(10,10),(0,10)),
        exception_classes=("CROSS_RED", "REVERSE_SHORT"),
        expiry_ms=50_000,
        policy_epoch=4,
        revocation_epoch=6,
        nonce="N-1",
        q_required=2,
        scene_epoch=3,
    )


def independent_evidence():
    return [
        SceneEvidence("credential","responder-system",True),
        SceneEvidence("vision","camera-local",True),
    ]


def test_two_independent_sources_satisfy_q2():
    assert corroborated(independent_evidence(), 2)


def test_two_channels_same_physical_source_count_once():
    ev = [SceneEvidence("radio","same-responder",True), SceneEvidence("app","same-responder",True)]
    assert not corroborated(ev, 2)


def test_valid_bounded_exception_allowed():
    a = authority()
    assert allow_emergency(authority=a, vehicle_id="AV-1", exception_class="CROSS_RED", position=(5,5), evidence=independent_evidence(), now_ms=10_000, current_policy_epoch=4, current_revocation_epoch=6, delta_loc=1, hard_safety_ok=True, consumed=False, revoked=False)


def test_wrong_vehicle_denied():
    a=authority()
    assert not allow_emergency(authority=a, vehicle_id="AV-2", exception_class="CROSS_RED", position=(5,5), evidence=independent_evidence(), now_ms=10_000, current_policy_epoch=4, current_revocation_epoch=6, delta_loc=1, hard_safety_ok=True, consumed=False, revoked=False)


def test_unlisted_exception_denied():
    a=authority()
    assert not allow_emergency(authority=a, vehicle_id="AV-1", exception_class="UNBOUNDED_REMOTE_DRIVE", position=(5,5), evidence=independent_evidence(), now_ms=10_000, current_policy_epoch=4, current_revocation_epoch=6, delta_loc=1, hard_safety_ok=True, consumed=False, revoked=False)


def test_scene_exit_denied():
    a=authority()
    assert not allow_emergency(authority=a, vehicle_id="AV-1", exception_class="CROSS_RED", position=(50,50), evidence=independent_evidence(), now_ms=10_000, current_policy_epoch=4, current_revocation_epoch=6, delta_loc=1, hard_safety_ok=True, consumed=False, revoked=False)


def test_expiry_denied():
    a=authority()
    assert not allow_emergency(authority=a, vehicle_id="AV-1", exception_class="CROSS_RED", position=(5,5), evidence=independent_evidence(), now_ms=50_001, current_policy_epoch=4, current_revocation_epoch=6, delta_loc=1, hard_safety_ok=True, consumed=False, revoked=False)


def test_revocation_epoch_change_denied():
    a=authority()
    assert not allow_emergency(authority=a, vehicle_id="AV-1", exception_class="CROSS_RED", position=(5,5), evidence=independent_evidence(), now_ms=10_000, current_policy_epoch=4, current_revocation_epoch=7, delta_loc=1, hard_safety_ok=True, consumed=False, revoked=False)


def test_hard_safety_failure_denied():
    a=authority()
    assert not allow_emergency(authority=a, vehicle_id="AV-1", exception_class="CROSS_RED", position=(5,5), evidence=independent_evidence(), now_ms=10_000, current_policy_epoch=4, current_revocation_epoch=6, delta_loc=1, hard_safety_ok=False, consumed=False, revoked=False)
