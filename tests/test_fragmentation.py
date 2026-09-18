from dataclasses import replace

from ef_ref.adversary import corrupt_fragment
from ef_ref.fragmentation import fragment_payload, reassemble


def test_complete_fragments_reassemble():
    key = b"k" * 32
    payload = b"execution-finality-proof" * 7
    fs = fragment_payload(payload, session_id="S1", key=key, mtu=17)
    assert reassemble(fs, key=key) == payload


def test_missing_fragment_is_incomplete():
    key = b"k" * 32
    fs = fragment_payload(b"abcdef" * 20, session_id="S1", key=key, mtu=11)
    assert reassemble(fs[:-1], key=key) is None


def test_mixed_session_rejected():
    key = b"k" * 32
    a = fragment_payload(b"A" * 80, session_id="S1", key=key, mtu=10)
    b = fragment_payload(b"B" * 80, session_id="S2", key=key, mtu=10)
    mixed = a[:]
    mixed[3] = b[3]
    assert reassemble(mixed, key=key) is None


def test_corrupted_fragment_rejected():
    key = b"k" * 32
    fs = fragment_payload(b"A" * 80, session_id="S1", key=key, mtu=10)
    fs[2] = corrupt_fragment(fs[2])
    assert reassemble(fs, key=key) is None


def test_wrong_key_rejected():
    fs = fragment_payload(b"A" * 80, session_id="S1", key=b"a" * 32, mtu=10)
    assert reassemble(fs, key=b"b" * 32) is None


def test_duplicate_index_rejected():
    key = b"k" * 32
    fs = fragment_payload(b"A" * 80, session_id="S1", key=key, mtu=10)
    fs[-1] = replace(fs[-1], index=0)
    assert reassemble(fs, key=key) is None
