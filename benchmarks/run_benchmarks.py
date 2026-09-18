from __future__ import annotations

import json
import os
import platform
import statistics
import sys
import time
from dataclasses import replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ef_ref.aer import EvidenceChain, Observer
from ef_ref.bpc import generate_bpc
from ef_ref.finality import FinalitySink
from ef_ref.fragmentation import fragment_payload, reassemble
from ef_ref.models import AuthorityState, CandidateAct


def pct(xs, p):
    ys=sorted(xs)
    return ys[min(len(ys)-1, max(0, int((p/100)*(len(ys)-1))))]


def summary(ns):
    us=[x/1000 for x in ns]
    return {"n":len(us),"p50_us":pct(us,50),"p95_us":pct(us,95),"p99_us":pct(us,99),"max_us":max(us),"mean_us":statistics.fmean(us)}


def timed(fn, n=2000):
    out=[]
    for i in range(n):
        t=time.perf_counter_ns(); fn(i); out.append(time.perf_counter_ns()-t)
    return summary(out)


def environment():
    return {
        "python":sys.version.split()[0],
        "platform":platform.platform(),
        "machine":platform.machine(),
        "processor":platform.processor(),
        "logical_cpus":os.cpu_count(),
        "implementation":"CPython local in-memory reference harness",
        "includes_network":False,
        "includes_secure_element_or_hsm":False,
        "includes_durable_fsync":False,
        "includes_actuator_io":False,
    }


def main():
    root=b"R"*32; sink_key=b"S"*32; session="bench-session"
    base=CandidateAct("uas:BENCH","a0","PAYLOAD_RELEASE","latch","{not-used}","AUTH",1,1,{"zone":"Z"},"n0",10**12)
    # repair params to dict (kept explicit to prevent accidental hidden setup)
    base=replace(base, params={"drop":"D","altitude_m":10})
    authority=AuthorityState("AUTH",("PAYLOAD_RELEASE",),"uas:BENCH",("latch",),1,1,10**12,{})

    gen = timed(lambda i: generate_bpc(replace(base, act_id=f"a{i}", nonce=f"n{i}"), root=root, session_nonce=session), 3000)

    pairs=[]
    for i in range(2500):
        a=replace(base, act_id=f"v{i}", nonce=f"vn{i}")
        pairs.append((a,generate_bpc(a,root=root,session_nonce=session)))
    sink=FinalitySink(root_key=root,sink_key=sink_key); sink.set_epochs(policy=1,revocation=1)
    idx=0
    def verify(_):
        nonlocal idx
        a,b=pairs[idx]; idx+=1
        d=sink.verify_and_effectuate(actual_act=a,bpc=b,authority=authority,session_nonce=session,now_ms=1000)
        if not d.allowed: raise RuntimeError(d.reason)
    verify_stats=timed(verify, len(pairs))

    c=EvidenceChain(k_seed=b"seed"*16,device_id="uas:BENCH",epoch_id="E1",chain_length=4096)
    aer_stats=timed(lambda i: c.make_aer(interval=i%4000,act_class="A",decision="ALLOW",sink_class="S",receipt_counter=i+1),3000)

    payload=b"X"*512; key=b"F"*32
    frag_stats=timed(lambda i: reassemble(fragment_payload(payload,session_id=f"S{i}",key=key,mtu=32),key=key),2000)

    result={
        "environment":environment(),
        "warning":"Local Python/in-memory measurements only; not actuator-grade or production latency.",
        "metrics":{
            "bpc_generation":gen,
            "finality_verify_consume_receipt_capability":verify_stats,
            "aer_generation":aer_stats,
            "fragment_512B_roundtrip":frag_stats,
        }
    }
    out=ROOT/"results"/"benchmark-results.json"
    out.write_text(json.dumps(result,indent=2,sort_keys=True))
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__ == "__main__":
    main()
