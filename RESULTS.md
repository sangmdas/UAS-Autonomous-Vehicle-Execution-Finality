# Packaged Verification Results

These are the results produced while packaging this reference repository. Re-run them on each target environment rather than treating these numbers as portable performance claims.

## Conformance / adversarial tests

```text
66 tests passed
```

The suite includes exact-act and sink substitution, replay, currentness races, receipt-store failure, 50-way concurrent single-use consumption, fragment loss/corruption/cross-session mixing, corrected AER interval-0 forgery resistance, late-record rejection, lost-KDR recovery, DAA stale conflict-set and Resolution-Epoch tests, emergency-scene independence tests, safe-state tests, and control-handover crash injection.

## Randomized handover red-team campaign

```text
seed: 20260918
iterations: 5000
dual-authority violations: 0
```

This is a property test of the included state machine, not a proof about an external OEM controller.

## Local Python benchmark snapshot

Environment captured by the benchmark harness:

```text
Python: 3.13.5
Machine: x86_64
Logical CPUs: 5
Network included: no
Secure element/HSM included: no
Durable fsync included: no
Actuator I/O included: no
```

Packaged-run latency (microseconds):

| Operation | p50 | p95 | p99 | max |
|---|---:|---:|---:|---:|
| BPC generation | 40.802 | 68.984 | 168.994 | 1104.711 |
| Finality verify + consume + in-memory receipt + capability | 81.212 | 191.128 | 297.468 | 2401.750 |
| AER generation | 3.766 | 3.986 | 6.931 | 892.021 |
| 512-byte fragmentation/reassembly roundtrip | 79.970 | 131.027 | 211.488 | 16910.797 |

**These are local reference-harness measurements, not production, real-time, airworthiness, ECU, actuator, or secure-element latency claims.** See `BENCHMARKS.md` and `results/benchmark-results.json`.
