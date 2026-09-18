# UAS / Autonomous-Vehicle Execution-Finality Reference

**Red-team-first reference implementation and conformance harness** for act-bound, sink-bound execution finality, constrained Beacon Proof Capsules (BPCs), delayed-disclosure Act Evidence Records (AER/KDR), conflict-set-bound DAA admission, emergency-scene temporary authority, and atomic control-authority handover.

> **Core rule:** computation, authentication, or possession of a token is not by itself effectuation authority. A consequential act remains non-effective until the protected effectuation boundary reconstructs the actual pending act, verifies current state, consumes freshness, commits evidence, and releases a bounded capability.

## What this repository is for

This repository turns architectural claims into falsifiable tests. The primary output is not a happy-path demo; it is evidence that specific invariants survive hostile mutation, replay, races, packet loss, stale state, crash points, and correlated evidence.

### Red mode

The default test philosophy assumes the upstream planner or mission computer can be hostile. The suite therefore tries to:

- change parameters after authorization;
- move a valid proof to another sink;
- replay a single-use act;
- advance policy or revocation state between pre-check and commit;
- delete, corrupt, duplicate, or cross-mix fragments;
- exploit the public AER chain commitment to forge interval 0;
- inject evidence after its secret is public;
- lose intermediate key disclosures;
- add a new DAA intruder after maneuver authorization;
- reuse a superseded Resolution Epoch;
- satisfy q-of-n with correlated scene reports;
- crash handover after PREPARE, COMMIT, or ENABLE;
- force concurrent consumes of the same nonce.

## Repository map

```text
src/ef_ref/       reference enforcement and evidence logic
spec/             concise architecture-specific descriptions
configs/          explicit test/system variables
tests/            positive + adversarial conformance tests
benchmarks/       local measurement harness
simulation/       scenario drivers
results/          generated local reports
test_vectors/     deterministic exchangeable vectors
```

## Quick start

```bash
python -m venv .venv
. .venv/bin/activate
pip install -e '.[test]'
pytest
python benchmarks/run_benchmarks.py
python simulation/red_team_campaign.py
```

No runtime cryptographic dependency is required beyond the Python standard library. The harness uses HMAC-SHA-256, SHA-256, and a minimal HKDF implementation for reproducibility.

## Corrected delayed-disclosure indexing

The repository uses a never-disclosed master seed distinct from discloseable chain values:

```text
K_seed  := protected master seed; never disclosed
K_N     := Trunc_128(H("UAS-AFE-seed" || K_seed || EpochID))
K_i     := F(K_(i+1))
K'_i    := F'(K_(i+1))       # AER tag key for evidence interval i
K_0     := public anchor commitment only
```

A record for interval `i` is accepted for later verification only if it arrived before the disclosure boundary. A later KDR can recover earlier required chain values through repeated application of `F`.

## Spatial revalidation example

```text
s_stop(v_max) = v_max*tau + v_max^2/(2*a_brk)
Delta_r <= (d(t) - epsilon_pos - s_stop(v_max)) / v_max
```

The included tests reproduce the illustrative 60 m / 30 m examples and verify that a non-positive bound removes further outward-motion authority.

## Test status

Run `pytest` to generate the authoritative local result. `results/test-summary.txt` records the last packaged run. The suite contains ordinary correctness tests plus red-team negative tests and a deterministic 5000-sequence handover crash campaign.

## Interpretation boundaries

Passing this harness demonstrates that the **reference state machine and cryptographic bindings** satisfy the tested invariants under the modeled adversary. It does not prove airworthiness, automotive functional safety, real-time deadlines, hardware non-bypassability, secure-element resistance, RF interoperability, or production readiness.

See `THREAT-MODEL.md`, `SYSTEM-VARIABLES.md`, `TEST-MATRIX.md`, `BENCHMARKS.md`, and `IPR-NOTICE.md` before drawing conclusions from results.


## License and patent-right separation

Unless a file states otherwise, the copyrightable contents of this repository are licensed under **CC BY-NC 4.0**. Non-commercial sharing and adaptation are permitted subject to attribution, license notice, and indication of changes. See `LICENSE.md`.

The copyright license does **not** grant a patent, SEP, FRAND, trademark, or commercial-use license. See `IPR-NOTICE.md`.

## What the repository does not prove

Passing the harness does not establish airworthiness, automotive functional safety, hardware non-bypassability, worst-case real-time behavior, formal cryptographic security, regulatory compliance, production readiness, patent validity, infringement, or standard essentiality. A verified AER is evidence of a protected decision record under the modeled construction; it is not by itself proof that a physical act occurred.

The complete limitations and interpretation boundaries are in `LIMITATIONS.md`.
