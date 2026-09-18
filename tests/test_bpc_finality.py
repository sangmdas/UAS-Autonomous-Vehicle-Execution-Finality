from __future__ import annotations

from dataclasses import replace
from concurrent.futures import ThreadPoolExecutor

from ef_ref.adversary import substitute_param, substitute_sink
from ef_ref.bpc import generate_bpc
from ef_ref.finality import FinalitySink
from ef_ref.receipt_store import ReceiptStore


def prepared(root_key, sink_key, session_nonce, baseline_act, authority):
    bpc = generate_bpc(baseline_act, root=root_key, session_nonce=session_nonce)
    sink = FinalitySink(root_key=root_key, sink_key=sink_key)
    sink.set_epochs(policy=7, revocation=9)
    return bpc, sink


def test_valid_act_allows(root_key, sink_key, session_nonce, baseline_act, authority):
    bpc, sink = prepared(root_key, sink_key, session_nonce, baseline_act, authority)
    d = sink.verify_and_effectuate(actual_act=baseline_act, bpc=bpc, authority=authority, session_nonce=session_nonce, now_ms=1_000_000)
    assert d.allowed and d.capability is not None and d.receipt_counter == 1


def test_replay_denied(root_key, sink_key, session_nonce, baseline_act, authority):
    bpc, sink = prepared(root_key, sink_key, session_nonce, baseline_act, authority)
    first = sink.verify_and_effectuate(actual_act=baseline_act, bpc=bpc, authority=authority, session_nonce=session_nonce, now_ms=1_000_000)
    second = sink.verify_and_effectuate(actual_act=baseline_act, bpc=bpc, authority=authority, session_nonce=session_nonce, now_ms=1_000_001)
    assert first.allowed
    assert not second.allowed and second.reason == "REPLAY"


def test_argument_substitution_denied(root_key, sink_key, session_nonce, baseline_act, authority):
    bpc, sink = prepared(root_key, sink_key, session_nonce, baseline_act, authority)
    attacked = substitute_param(baseline_act, "drop_zone", "DZ-ATTACK")
    d = sink.verify_and_effectuate(actual_act=attacked, bpc=bpc, authority=authority, session_nonce=session_nonce, now_ms=1_000_000)
    assert not d.allowed and d.reason in {"ACT_MISMATCH", "CONTEXT_MISMATCH", "BINDING_MISMATCH"}


def test_sink_substitution_denied(root_key, sink_key, session_nonce, baseline_act, authority):
    bpc, sink = prepared(root_key, sink_key, session_nonce, baseline_act, authority)
    attacked = substitute_sink(baseline_act, "motor-esc-7")
    d = sink.verify_and_effectuate(actual_act=attacked, bpc=bpc, authority=authority, session_nonce=session_nonce, now_ms=1_000_000)
    assert not d.allowed and d.reason == "SINK_MISMATCH"


def test_context_substitution_denied(root_key, sink_key, session_nonce, baseline_act, authority):
    bpc, sink = prepared(root_key, sink_key, session_nonce, baseline_act, authority)
    attacked = replace(baseline_act, context={**baseline_act.context, "geofence":"G99"})
    d = sink.verify_and_effectuate(actual_act=attacked, bpc=bpc, authority=authority, session_nonce=session_nonce, now_ms=1_000_000)
    assert not d.allowed and d.reason in {"ACT_MISMATCH", "CONTEXT_MISMATCH", "BINDING_MISMATCH"}


def test_expired_denied(root_key, sink_key, session_nonce, baseline_act, authority):
    bpc, sink = prepared(root_key, sink_key, session_nonce, baseline_act, authority)
    d = sink.verify_and_effectuate(actual_act=baseline_act, bpc=bpc, authority=authority, session_nonce=session_nonce, now_ms=2_000_001)
    assert not d.allowed and d.reason == "EXPIRED"


def test_policy_change_after_precheck_denied_at_commit(root_key, sink_key, session_nonce, baseline_act, authority):
    bpc, sink = prepared(root_key, sink_key, session_nonce, baseline_act, authority)
    def race():
        sink.set_epochs(policy=8)
    d = sink.verify_and_effectuate(actual_act=baseline_act, bpc=bpc, authority=authority, session_nonce=session_nonce, now_ms=1_000_000, pre_commit_hook=race)
    assert not d.allowed and d.reason == "POLICY_EPOCH_MISMATCH"


def test_revocation_change_after_precheck_denied_at_commit(root_key, sink_key, session_nonce, baseline_act, authority):
    bpc, sink = prepared(root_key, sink_key, session_nonce, baseline_act, authority)
    def race():
        sink.set_epochs(revocation=10)
    d = sink.verify_and_effectuate(actual_act=baseline_act, bpc=bpc, authority=authority, session_nonce=session_nonce, now_ms=1_000_000, pre_commit_hook=race)
    assert not d.allowed and d.reason == "REVOCATION_EPOCH_MISMATCH"


def test_receipt_store_failure_fails_closed(root_key, sink_key, session_nonce, baseline_act, authority):
    store = ReceiptStore(); store.available = False
    bpc = generate_bpc(baseline_act, root=root_key, session_nonce=session_nonce)
    sink = FinalitySink(root_key=root_key, sink_key=sink_key, receipt_store=store)
    sink.set_epochs(policy=7, revocation=9)
    d = sink.verify_and_effectuate(actual_act=baseline_act, bpc=bpc, authority=authority, session_nonce=session_nonce, now_ms=1_000_000)
    assert not d.allowed and d.reason == "RECEIPT_STORE_UNAVAILABLE" and d.capability is None
    assert baseline_act.nonce in sink.replay.snapshot()


def test_receipt_failure_retry_does_not_effectuate(root_key, sink_key, session_nonce, baseline_act, authority):
    store = ReceiptStore(); store.available = False
    bpc = generate_bpc(baseline_act, root=root_key, session_nonce=session_nonce)
    sink = FinalitySink(root_key=root_key, sink_key=sink_key, receipt_store=store)
    sink.set_epochs(policy=7, revocation=9)
    one = sink.verify_and_effectuate(actual_act=baseline_act, bpc=bpc, authority=authority, session_nonce=session_nonce, now_ms=1_000_000)
    store.available = True
    two = sink.verify_and_effectuate(actual_act=baseline_act, bpc=bpc, authority=authority, session_nonce=session_nonce, now_ms=1_000_001)
    assert not one.allowed
    assert not two.allowed and two.reason == "REPLAY"


def test_50_way_same_nonce_concurrency_allows_exactly_once(root_key, sink_key, session_nonce, baseline_act, authority):
    bpc, sink = prepared(root_key, sink_key, session_nonce, baseline_act, authority)
    def run(_):
        return sink.verify_and_effectuate(actual_act=baseline_act, bpc=bpc, authority=authority, session_nonce=session_nonce, now_ms=1_000_000)
    with ThreadPoolExecutor(max_workers=16) as ex:
        results = list(ex.map(run, range(50)))
    assert sum(1 for r in results if r.allowed) == 1
    assert sum(1 for r in results if r.reason == "REPLAY") == 49
