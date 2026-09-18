from dataclasses import replace

from ef_ref.aer import EvidenceChain, Observer
from ef_ref.adversary import retag_aer_with_public_anchor


def chain():
    return EvidenceChain(k_seed=b"master-seed-never-disclosed" * 2, device_id="uas:TEST-1", epoch_id="E7", chain_length=16, interval_ms=1000, delay_intervals=3)


def test_master_seed_is_distinct_from_terminal_chain_value():
    c = chain()
    assert c.k_seed != c._keys[c.N]


def test_public_k0_cannot_derive_interval0_valid_tag():
    c = chain()
    aer = c.make_aer(interval=0, act_class="PAYLOAD_RELEASE", decision="ALLOW", sink_class="LATCH", receipt_counter=1)
    forged = retag_aer_with_public_anchor(aer, c.anchor_k0)
    obs = Observer(device_id=c.device_id, epoch_id=c.epoch_id, anchor_k0=c.anchor_k0, delay_intervals=c.delay, interval_ms=c.interval_ms)
    assert obs.receive_aer(forged, receive_time_ms=500)
    assert obs.receive_kdr(c.disclose_for_interval(0)) == []


def test_valid_interval0_verifies_after_disclosure():
    c = chain(); obs = Observer(device_id=c.device_id, epoch_id=c.epoch_id, anchor_k0=c.anchor_k0, delay_intervals=3, interval_ms=1000)
    aer = c.make_aer(interval=0, act_class="PAYLOAD_RELEASE", decision="ALLOW", sink_class="LATCH", receipt_counter=1)
    assert obs.receive_aer(aer, receive_time_ms=500)
    assert obs.receive_kdr(c.disclose_for_interval(0)) == [aer]


def test_late_record_rejected_even_if_tag_valid():
    c = chain(); obs = Observer(device_id=c.device_id, epoch_id=c.epoch_id, anchor_k0=c.anchor_k0, delay_intervals=3, interval_ms=1000)
    aer = c.make_aer(interval=0, act_class="PAYLOAD_RELEASE", decision="ALLOW", sink_class="LATCH", receipt_counter=1)
    assert not obs.receive_aer(aer, receive_time_ms=3000)


def test_loss_of_intermediate_kdr_recovered_by_later_disclosure():
    c = chain(); obs = Observer(device_id=c.device_id, epoch_id=c.epoch_id, anchor_k0=c.anchor_k0, delay_intervals=3, interval_ms=1000)
    a0 = c.make_aer(interval=0, act_class="A", decision="ALLOW", sink_class="S", receipt_counter=1)
    a1 = c.make_aer(interval=1, act_class="A", decision="ALLOW", sink_class="S", receipt_counter=2)
    a2 = c.make_aer(interval=2, act_class="A", decision="DENY", sink_class="S", receipt_counter=3)
    assert obs.receive_aer(a0, receive_time_ms=100)
    assert obs.receive_aer(a1, receive_time_ms=1100)
    assert obs.receive_aer(a2, receive_time_ms=2100)
    verified = obs.receive_kdr(c.disclose_for_interval(2))
    assert verified == [a0, a1, a2]


def test_wrong_epoch_record_rejected():
    c = chain(); obs = Observer(device_id=c.device_id, epoch_id=c.epoch_id, anchor_k0=c.anchor_k0, delay_intervals=3, interval_ms=1000)
    aer = c.make_aer(interval=0, act_class="A", decision="ALLOW", sink_class="S", receipt_counter=1)
    assert not obs.receive_aer(replace(aer, epoch_id="WRONG"), receive_time_ms=100)


def test_wrong_device_record_rejected():
    c = chain(); obs = Observer(device_id=c.device_id, epoch_id=c.epoch_id, anchor_k0=c.anchor_k0, delay_intervals=3, interval_ms=1000)
    aer = c.make_aer(interval=0, act_class="A", decision="ALLOW", sink_class="S", receipt_counter=1)
    assert not obs.receive_aer(replace(aer, device_id="uas:OTHER"), receive_time_ms=100)


def test_wrong_kdr_key_rejected():
    c = chain(); obs = Observer(device_id=c.device_id, epoch_id=c.epoch_id, anchor_k0=c.anchor_k0, delay_intervals=3, interval_ms=1000)
    aer = c.make_aer(interval=0, act_class="A", decision="ALLOW", sink_class="S", receipt_counter=1)
    assert obs.receive_aer(aer, receive_time_ms=100)
    kdr = c.disclose_for_interval(0)
    bad = replace(kdr, key=b"X" * len(kdr.key))
    assert obs.receive_kdr(bad) == []


def test_tag_key_not_chain_member():
    c = chain()
    assert c.tag_key(0) not in c._keys
