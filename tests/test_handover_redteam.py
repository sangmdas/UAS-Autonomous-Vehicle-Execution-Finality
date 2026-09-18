import random

import pytest

from ef_ref.handover import HandoverController, InjectedCrash
from ef_ref.models import ControlState


def ctl():
    return HandoverController(ControlState("motion-sink", "AUTONOMY", 31, {"min":-1.0,"max":1.0}))


def test_old_controller_before_handover_valid():
    c=ctl()
    assert c.accepts(controller="AUTONOMY", epoch=31, sink_id="motion-sink", act_value=0.2)


def test_prepare_does_not_enable_new_controller():
    c=ctl(); c.prepare("REMOTE")
    assert not c.accepts(controller="REMOTE", epoch=32, sink_id="motion-sink", act_value=0)
    assert c.accepts(controller="AUTONOMY", epoch=31, sink_id="motion-sink", act_value=0)


def test_commit_creates_safe_only_gap_not_dual_authority():
    c=ctl(); c.prepare("REMOTE"); c.commit()
    assert not c.accepts(controller="AUTONOMY", epoch=31, sink_id="motion-sink", act_value=0)
    assert not c.accepts(controller="REMOTE", epoch=32, sink_id="motion-sink", act_value=0)
    assert c.state.safe_only


def test_enable_switches_exclusively_to_new_controller():
    c=ctl(); c.prepare("REMOTE"); c.commit(); c.enable()
    assert not c.accepts(controller="AUTONOMY", epoch=31, sink_id="motion-sink", act_value=0)
    assert c.accepts(controller="REMOTE", epoch=32, sink_id="motion-sink", act_value=0)

@pytest.mark.parametrize("point", ["after_prepare","after_commit","after_enable"])
def test_crash_injection_never_yields_dual_authority(point):
    c=ctl()
    with pytest.raises(InjectedCrash):
        c.transactional_handover("REMOTE", crash_at=point)
    contenders=[("AUTONOMY",31),("REMOTE",32)]
    assert c.effective_authority_count(contenders) <= 1


def test_old_epoch_rejected_after_complete_handover():
    c=ctl(); c.transactional_handover("REMOTE")
    assert not c.accepts(controller="REMOTE", epoch=31, sink_id="motion-sink", act_value=0)


def test_envelope_violation_rejected():
    c=ctl()
    assert not c.accepts(controller="AUTONOMY", epoch=31, sink_id="motion-sink", act_value=2.0)


def test_randomized_handover_sequences_preserve_exclusivity():
    rng=random.Random(20260918)
    for _ in range(1000):
        c=ctl()
        point=rng.choice([None,"after_prepare","after_commit","after_enable"])
        try:
            c.transactional_handover("REMOTE", crash_at=point)
        except InjectedCrash:
            pass
        assert c.effective_authority_count([("AUTONOMY",31),("REMOTE",32)]) <= 1
