from __future__ import annotations

import json
import sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ef_ref.aer import EvidenceChain
from ef_ref.bpc import generate_bpc
from ef_ref.crypto import canonical_bytes
from ef_ref.fragmentation import fragment_payload
from ef_ref.models import CandidateAct


def hx(v):
    return v.hex() if isinstance(v, bytes) else v


def serial(d):
    return {k: hx(v) for k,v in d.items()}


def main():
    act = CandidateAct(
        device_id="uas:VECTOR-1", act_id="act-vector-1", act_class="PAYLOAD_RELEASE",
        sink_id="latch-1", params={"drop_zone":"DZ-1","altitude_m":10}, authority_ref="AUTH-V1",
        policy_epoch=3, revocation_epoch=5, context={"geofence":"G1","phase":"DELIVERY"},
        nonce="nonce-vector-1", expiry_ms=2_000_000,
    )
    root = bytes.fromhex("01"*32)
    bpc = generate_bpc(act, root=root, session_nonce="vector-session", binding_bits=96, tag_bits=96)
    (ROOT/"test_vectors"/"bpc"/"baseline.json").write_text(json.dumps({
        "candidate_act": act.to_dict(),
        "root_key_hex": root.hex(),
        "session_nonce":"vector-session",
        "bpc": serial(asdict(bpc)),
    }, indent=2, sort_keys=True))

    payload = canonical_bytes({"proof":"fragment-vector","counter":7,"act":"PAYLOAD_RELEASE"})
    fragments = fragment_payload(payload, session_id="frag-vector", key=bytes.fromhex("02"*32), mtu=12)
    (ROOT/"test_vectors"/"fragmentation"/"baseline.json").write_text(json.dumps({
        "payload_hex":payload.hex(),
        "key_hex":"02"*32,
        "fragments":[serial(asdict(f)) for f in fragments],
    }, indent=2, sort_keys=True))

    c = EvidenceChain(k_seed=bytes.fromhex("03"*32), device_id="uas:VECTOR-1", epoch_id="EV-1", chain_length=8, interval_ms=1000, delay_intervals=3)
    aer = c.make_aer(interval=0, act_class="PAYLOAD_RELEASE", decision="ALLOW", sink_class="LATCH", receipt_counter=1)
    kdr = c.disclose_for_interval(0)
    (ROOT/"test_vectors"/"aer"/"interval0.json").write_text(json.dumps({
        "master_seed_hex":"03"*32,
        "device_id":c.device_id,
        "epoch_id":c.epoch_id,
        "N":c.N,
        "K_N_hex":c._keys[c.N].hex(),
        "K_0_hex":c.anchor_k0.hex(),
        "K_prime_0_hex":c.tag_key(0).hex(),
        "aer":serial(asdict(aer)),
        "kdr":serial(asdict(kdr)),
    }, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
