from __future__ import annotations

import json
import random
from dataclasses import asdict

from ef_ref.handover import HandoverController, InjectedCrash
from ef_ref.models import ControlState


def run(seed: int = 20260918, iterations: int = 5000) -> dict:
    rng = random.Random(seed)
    dual_authority_violations = 0
    states = {"complete":0, "after_prepare":0, "after_commit":0, "after_enable":0}
    for _ in range(iterations):
        state = ControlState("motion-sink", "AUTONOMY", 31, {"min":-1.0,"max":1.0})
        ctl = HandoverController(state)
        point = rng.choice([None,"after_prepare","after_commit","after_enable"])
        key = "complete" if point is None else point
        states[key] += 1
        try:
            ctl.transactional_handover("REMOTE", crash_at=point)
        except InjectedCrash:
            pass
        if ctl.effective_authority_count([("AUTONOMY",31),("REMOTE",32)]) > 1:
            dual_authority_violations += 1
    return {"seed":seed, "iterations":iterations, "dual_authority_violations":dual_authority_violations, "schedule_distribution":states}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
