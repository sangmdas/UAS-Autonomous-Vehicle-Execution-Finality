# Red-Team Mode

Red-Team Mode treats every upstream representation as potentially adversarial until the protected effectuation boundary reconstructs and verifies the concrete pending act.

## 1. Campaign classes

### RT-A — Semantic substitution
Attack the meaning of an already-authenticated request without necessarily breaking its transport authentication.

Variables:
- act class
- sink identifier
- payload/drop zone
- trajectory or speed envelope
- device identifier
- authority reference
- policy epoch
- revocation epoch
- context/geofence
- nonce/freshness
- expiry

Pass condition: any load-bearing change produces denial before capability release.

### RT-B — Time-of-check / time-of-effect races

Sequence:

```text
1. Perform an early/preliminary verification.
2. Advance protected policy or revocation state.
3. Attempt the final atomic consume.
4. Assert that the deciding read sees the new epoch and denies the stale act.
```

Pass condition: an earlier successful read never overrides the final protected currentness read.

### RT-C — Replay and concurrency

The suite concurrently submits the same single-use nonce 50 times. The property is:

```text
ALLOW_count == 1
REPLAY_count == attempts - 1
```

This should be repeated with higher thread counts and, in a production port, across process, host, and failover boundaries.

### RT-D — Fragmentation / constrained transport

Attacks:
- missing fragment;
- duplicate fragment index;
- corrupted fragment payload;
- cross-session fragment insertion;
- wrong fragment authentication key;
- fragment reorder;
- mismatched root / total count.

Pass condition: incomplete or mixed evidence never progresses to effectuation verification.

### RT-E — Delayed-disclosure evidence

The campaign specifically tests the corrected index convention:

```text
K_seed = never-disclosed master secret
K_N = derived terminal chain value
K_0 = public anchor
AER interval i uses K'_i = F'(K_(i+1))
```

Attacks:
- attempt interval-0 forgery using public K_0 and F'(K_0);
- inject a valid old AER only after its key is public;
- wrong DeviceID;
- wrong EpochID;
- malformed/wrong KDR key;
- lost intermediate KDRs;
- duplicate/old disclosure.

Pass conditions:
- public K_0 cannot generate a valid interval-0 record;
- late records are discarded even if their tag is mathematically valid;
- a later authentic KDR can recover earlier undisclosed chain values needed for retained records.

### RT-F — DAA stale-basis attacks

Attacks:
- authorize with conflict set C1, then add a new relevant intruder;
- modify a track state;
- age a track beyond freshness limit;
- supersede the Resolution Epoch;
- redirect the maneuver to another motion sink;
- construct a maneuver safe for one intruder but unsafe for another.

Pass condition: acceptance requires current Conflict-Set Root, current Resolution Epoch, correct sink, fresh relevant tracks, and all-intruder safety under the profile predicate.

### RT-G — Emergency-scene authority laundering

Attacks:
- two channels derived from one physical source presented as q=2;
- wrong vehicle;
- unlisted traffic-rule exception;
- position outside the dilated scene;
- expired authority;
- policy/revocation epoch change;
- failed hard-safety predicate.

Pass condition: temporary authority stays bounded and extinguishes when any required state no longer holds.

### RT-H — Control-authority split brain

Crash points:

```text
PREPARE -> crash
COMMIT  -> crash
ENABLE  -> crash
```

Property:

```text
for all observed states:
    effective_authority_count <= 1
```

The deterministic randomized campaign executes 5,000 schedules in the packaged run. The unit test executes an additional 1,000 seeded sequences.

## 2. Fault-injection expansion for real hardware

A platform port should add faults not modeled in this pure-Python harness:

- reset during flash/FRAM replay-state update;
- torn persistent receipt write;
- brownout between capability generation and hardware latch;
- DMA write attempts around the protected gateway;
- bus-master bypass of the sink;
- stale cache after failover;
- dual-controller network partition;
- clock step and clock rollback;
- GNSS loss/spoofing and source-correlation attacks;
- packet burst loss and reordering;
- secure-element/HSM timeout;
- watchdog reset inside atomic transition;
- actuator acknowledgement loss;
- ECU/flight-controller firmware rollback.

Each hardware campaign should record the exact failure-injection point and persistent state before/after reboot.

## 3. Randomization variables

Recommended seeded fuzz ranges:

| Variable | Example range |
|---|---|
| act parameter mutations | 1–8 fields |
| concurrent duplicate submissions | 2–1,000 |
| packet loss | 0–40% |
| packet reordering | 0–20% |
| AER disclosure delay | 1–10 intervals |
| observer clock uncertainty | 0–2 intervals |
| DAA intruders | 0–50 |
| track age | 0–5,000 ms |
| uncertainty | 0–100 m |
| handover crash point | every protected state transition |
| q-of-n scene threshold | 1–5 |
| evidence-source correlation | 0–100% |

Every randomized run should publish the seed so a failure can be replayed exactly.

## 4. Success criteria

A run is considered successful only when:

1. no consequential act is allowed after a required binding/currentness predicate fails;
2. no duplicate single-use consume produces a second capability;
3. no failed receipt commit produces a capability;
4. no partial/mixed fragment set becomes verification input;
5. no public AER anchor value acts as a pre-disclosure signing secret;
6. no stale DAA basis is admitted after the relevant conflict state changes;
7. no q-of-n rule can be met merely by duplicating one physical evidence source;
8. no handover crash state gives two ordinary controllers simultaneous effectuation authority;
9. safe-action paths remain separately available where the profile requires safety asymmetry.

## 5. What Red-Team Mode cannot prove

The harness cannot prove physical non-bypassability. A real deployment must separately demonstrate that there is no alternative actuator, debug, DMA, bus, maintenance, or emergency path that can create the protected effect without traversing the Finality Sink. It also cannot substitute for hazard analysis, airworthiness certification, ISO 26262/SOTIF work, DO-178C/DO-254 assurance, cybersecurity certification, or regulatory approval.
