from ef_ref.bpc import derive_session_keys


def test_bpc_auth_and_binding_keys_are_separate(root_key):
    kb,kbind=derive_session_keys(root_key,session_nonce="s",device_id="d",policy_epoch=1,sink_id="x")
    assert kb != kbind


def test_sink_scope_changes_binding_key(root_key):
    _,a=derive_session_keys(root_key,session_nonce="s",device_id="d",policy_epoch=1,sink_id="x")
    _,b=derive_session_keys(root_key,session_nonce="s",device_id="d",policy_epoch=1,sink_id="y")
    assert a != b
