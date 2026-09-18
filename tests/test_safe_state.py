def safe_action_available(action: str, safe_set: set[str], ordinary_authority_valid: bool) -> bool:
    if action in safe_set:
        return True
    return ordinary_authority_valid


def test_brake_remains_available_when_ordinary_authority_fails():
    safe={"BRAKE","MINIMAL_RISK_STOP","HOVER","LAND"}
    assert safe_action_available("BRAKE", safe, False)


def test_permission_expansion_not_safe_by_default():
    safe={"BRAKE","MINIMAL_RISK_STOP"}
    assert not safe_action_available("INCREASE_SPEED_ENVELOPE", safe, False)
