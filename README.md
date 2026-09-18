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


## EXPANDED VERSION OF README

Below is a stronger expanded README version that keeps the same structure but makes the repository look much more complete, technical, and reviewable.

# UAS / Autonomous-Vehicle Execution-Finality Reference

**Red-team-first reference implementation and conformance harness** for act-bound, sink-bound execution finality, constrained Beacon Proof Capsules (BPCs), delayed-disclosure Act Evidence Records (AER/KDR), conflict-set-bound Detect-and-Avoid (DAA) admission, emergency-scene temporary authority, and atomic control-authority handover.

> **Core rule:** computation, authentication, successful policy evaluation, or possession of a token is not by itself effectuation authority. A consequential act remains non-effective until the protected effectuation boundary reconstructs the actual pending act, verifies current protected state, consumes freshness, commits evidence, and releases a bounded capability.

The repository is intended to make execution-finality claims **concrete, falsifiable, reproducible, and open to adversarial review**.

It is not structured primarily as a demonstration of successful execution. It is structured to answer a harder question:

> **What happens when an attacker, stale state, packet loss, crash, race, substituted parameter, superseded authority, or alternate control path tries to make a different act become effective?**

---

## What this repository is for

The repository converts architectural invariants into executable state machines, cryptographic bindings, test vectors, adversarial tests, and measurable software paths.

The central verification model is:

```text
architectural invariant
        |
        v
adversarial condition
        |
        v
expected protected response
        |
        v
automated test
        |
        v
measured / reproducible result
```

The objective is not merely to show that the intended path works.

The objective is to test whether the implementation fails safely when the surrounding system behaves incorrectly or maliciously.

Representative invariants include:

```text
No verified proof              -> no effectuation
Changed act                    -> binding mismatch
Changed sink                   -> sink mismatch
Consumed nonce                 -> replay denied
Stale policy / revocation      -> effectuation denied
Missing fragment               -> incomplete, not authority
Ambiguous compact commitment   -> deny or escalate
Receipt-store failure          -> no release
AER / KDR / receipt            -> evidence only, never authority
Superseded DAA resolution      -> motion admission denied
Stale controller epoch         -> command denied
Authority handover             -> at most one effective controller
Safe-state path                -> remains available where defined
```

---

## Threat model

The harness intentionally assumes that substantial parts of the upstream system may be hostile or unreliable.

The following components are not automatically trusted merely because they are authenticated or privileged:

* mission computer;
* autonomous planner;
* AI/ML component;
* navigation software;
* application processor;
* remote operator interface;
* fleet-management service;
* command transmitter;
* network transport;
* cached authority data;
* unprotected logging system;
* ordinary operating-system process;
* caller-supplied Candidate Act representation.

The Protected Enforcement Domain and Finality Sink are modeled as the components responsible for independently determining whether the actual pending effect is authorized.

The repository therefore does not assume:

```text
authenticated command = authorized act
signed command        = safe act
valid token           = current authority
successful planning   = permission to actuate
verified identity     = permission to produce every effect
```

Instead:

```text
proposal
   |
   v
Candidate Act
   |
   v
Non-Effective State
   |
   v
protected reconstruction + current-state verification
   |
   v
atomic consume + receipt commit
   |
   v
bounded release capability
   |
   v
Finality Sink
   |
   v
effectuation
```

---

## Red mode

The default test philosophy assumes the upstream planner or mission computer can be hostile.

The test suite therefore attempts to:

* change action parameters after authorization;
* alter coordinates, target state, route, payload parameters, timing, or envelope limits;
* move an otherwise valid proof to another Finality Sink;
* copy authorization between aircraft, vehicles, actuators, or sessions;
* replay a single-use Candidate Act;
* issue the same nonce concurrently from multiple threads;
* advance policy state after an early validation step;
* advance revocation state between pre-check and atomic consume;
* force stale cached authority into the hot path;
* delete, corrupt, duplicate, reorder, or cross-mix BPC fragments;
* substitute a fragment from another session;
* create incomplete fragment sets;
* trigger compact-commitment ambiguity;
* exploit a public AER chain commitment to forge the first evidence interval;
* generate evidence after the corresponding delayed-disclosure secret is public;
* suppress one or more Key Disclosure Records;
* inject KDRs out of sequence;
* transplant AERs between evidence epochs;
* transplant AERs between device identities;
* introduce a new DAA intruder after maneuver authorization;
* change a conflict set after a resolution has been computed;
* replay a superseded Resolution Epoch;
* create multiple simultaneously plausible DAA resolutions;
* satisfy q-of-n emergency-scene corroboration using correlated evidence;
* keep emergency-scene authority alive after scene expiry;
* use stale responder authority after Scene Epoch advancement;
* crash authority handover after PREPARE;
* crash after COMMIT but before ENABLE;
* replay commands from a previous Control Authority Epoch;
* attempt split-brain controller activation;
* cause receipt persistence failure;
* force effectuation after incomplete state transition;
* attempt effectuation through an alternate modeled sink path.

The expected result is normally not “recover and continue.”

For high-assurance paths, the expected result is generally:

```text
DENY
HOLD
SAFE STATE
REVALIDATE
REQUEST LONGER PROOF
REQUEST CURRENT AUTHORITY
```

depending on the modeled profile.

---

## Repository map

```text
src/ef_ref/
    Core reference enforcement and evidence logic.

spec/
    Concise descriptions of the modeled architecture and
    profile-specific behavior.

configs/
    Explicit deployment, cryptographic, timing, risk,
    spatial, DAA, AER, and system variables.

tests/
    Positive-path, negative-path, adversarial,
    concurrency, race, and failure-injection tests.

simulation/
    Scenario drivers and red-team campaigns.

benchmarks/
    Local software latency and throughput measurements.

test_vectors/
    Deterministic BPC, fragmentation, AER, and KDR vectors.

results/
    Reproducible local test and benchmark outputs.

README.md
ARCHITECTURE.md
THREAT-MODEL.md
RED-TEAM-MODE.md
FAULT-INJECTION.md
SYSTEM-VARIABLES.md
TEST-MATRIX.md
BENCHMARKS.md
RESULTS.md
LIMITATIONS.md
SECURITY.md
IPR-NOTICE.md
LICENSE.md
```

The repository is intentionally split so that test assumptions are not hidden inside implementation code.

Security-significant values are exposed through explicit configuration wherever practical.

---

## Quick start

```bash
python -m venv .venv
. .venv/bin/activate

pip install -e '.[test]'

pytest

python benchmarks/run_benchmarks.py

python simulation/red_team_campaign.py
```

The reference harness uses Python for readability and reproducibility.

No runtime cryptographic dependency is required beyond the Python standard library for the packaged reference construction. The implementation uses:

```text
SHA-256
HMAC-SHA-256
minimal HKDF construction
deterministic canonical representations
constant-format test vectors
```

The implementation is intentionally not optimized as a production cryptographic library.

---

# Core execution-finality model

## Candidate Act

A Candidate Act is a proposed operation capable of producing a physical, operational, communicative, persistent, or otherwise externally consequential effect.

Examples include:

```text
arm propulsion
release payload
enter restricted volume
change trajectory
activate sensor
emit RF energy
change autonomous mode
accept coordinated maneuver
admit steering / braking / propulsion envelope
```

The important distinction is that a Candidate Act may already have been:

```text
computed
selected
signed
received
approved upstream
transmitted
validated in part
```

and still remain non-effective.

---

## Finality Sink

A Finality Sink is the boundary at which an operation can still be prevented from becoming effective.

Representative examples include:

```text
ESC enable
motor-output gate
payload-latch controller
RF transmit-enable gate
camera / sensor enable
trajectory-admission gate
drive-by-wire admission
vehicle motion controller
protected actuator gateway
```

The reference implementation treats the Finality Sink as the component that independently compares the authorization basis against the **actual pending act**, rather than relying only on a caller-supplied description.

---

## Non-Effective State

The repository models the rule:

```text
Candidate Act exists
        !=
Candidate Act can produce its external effect
```

A proposed act remains non-effective until the required protected transition occurs.

Conceptually:

```text
Candidate Act
     |
     v
[ Non-Effective State ]
     |
     | verify actual act
     | verify sink
     | verify authority
     | verify freshness
     | verify current epochs
     | consume replay state
     | commit receipt
     v
[ bounded capability ]
     |
     v
Finality Sink
     |
     v
Effect
```

---

# Act-bound and sink-bound authorization

The architecture does not treat authorization as a generic bearer permission.

A binding commitment may include:

```text
Candidate Act digest
Finality Sink
Authority Reference
Policy Epoch
Revocation Epoch
Context Commitment
Nonce / freshness
Expiry
```

Representative construction:

```text
D_A = H(DOM_A || Canonical(CandidateAct))

D_C = H(DOM_C || Canonical(Context))

B = HMAC_Kbind(
      DOM_B ||
      D_A ||
      SinkID ||
      AuthorityRef ||
      PolicyEpoch ||
      RevocationEpoch ||
      D_C ||
      Freshness ||
      Expiry
    )
```

A material change to the impending act therefore produces a different binding basis.

The sink reconstructs or observes the actual pending act rather than trusting the upstream caller to tell it what will happen.

---

# Beacon Proof Capsules

Beacon Proof Capsules are modeled as compact verification objects for constrained communication paths.

A BPC may contain or reference:

```text
version
profile
act class
sink class
Authority Reference
policy generation
revocation generation
freshness
expiry
context commitment
compact binding commitment
authenticator
fragment information
```

A BPC is **not itself effectuation authority merely because it exists or has been received**.

The protected verifier still evaluates the actual impending act.

---

## Truncated commitment sizing

The repository includes explicit variables for compact-commitment risk.

For approximately `q` commitments within the relevant collision domain:

```text
P_coll ~= q(q-1) / 2^(t+1)
```

A corresponding lower bound is:

```text
t >= ceil(
       log2(
         q(q-1) / (2 * epsilon_c)
       )
     )
```

For an unkeyed value exposed to offline search:

```text
P_sub ~= W / 2^t
```

where `W` is an assumed attacker work budget.

For a keyed construction where only bounded online attempts are available:

```text
P_sub <= A_online / 2^t
```

The repository therefore treats truncation length as a security parameter rather than simply a packet-size preference.

---

# Authenticated fragmentation

Where the compact proof cannot fit in one transport unit, the reference construction models authenticated fragmentation.

Conceptually:

```text
P = p_0 || p_1 || ... || p_(n-1)

Root = SHA-256(
         "UAS-BPC-FRAG-ROOT" || P
       )
```

Each fragment is bound to:

```text
SessionID
Root
fragment index
fragment count
fragment payload
```

The red-team suite exercises:

```text
missing fragment
duplicate fragment
wrong index
wrong count
wrong root
wrong session
fragment substitution
cross-session mixing
reordering
corruption
```

An incomplete reconstruction does not become authority.

---

# Corrected delayed-disclosure indexing

The repository uses a never-disclosed master seed distinct from discloseable chain values.

```text
K_seed := protected master seed
          never disclosed

K_N := Trunc_128(
         H(
           "UAS-AFE-seed" ||
           K_seed ||
           EpochID
         )
       )

K_i := F(K_(i+1))

K'_i := F'(K_(i+1))
        # AER tag key for evidence interval i

K_0 := public chain commitment only
```

Representative domain-separated functions are:

```text
F(x) =
    Trunc_128(
      SHA-256(
        "UAS-AFE-chain" || x
      )
    )

F'(x) =
    Trunc_128(
      SHA-256(
        "UAS-AFE-tag" || x
      )
    )
```

AER interval `i` therefore uses:

```text
K'_i = F'(K_(i+1))
```

and later discloses:

```text
K_(i+1)
```

after the configured delay.

The public value `K_0` is only the chain commitment.

It is not an AER authentication secret and is not used through `F'` to generate the first interval's authentication key.

---

## AER authentication

Representative AER authentication is:

```text
TAG_i =
  Trunc_m(
    HMAC_K'_i(
      DOM_E ||
      DeviceID ||
      EpochID ||
      Header_i
    )
  )
```

The Act Evidence Record may then be:

```text
Header_i || TAG_i
```

The model distinguishes sharply between:

```text
execution authority
```

and:

```text
evidence that a protected decision was made
```

An AER is never accepted as an execution capability.

---

## Delayed-disclosure safety condition

A record received after its verification secret may already have become public cannot establish pre-disclosure origin.

The observer therefore applies a timing rule.

For:

```text
T_0       evidence epoch start
Delta     interval duration
d         disclosure delay
delta_max clock uncertainty bound
t_r       record receive time
```

the observer calculates the corresponding safety interval and rejects records that may have been created only after disclosure.

The negative tests explicitly attempt:

```text
post-disclosure forgery
late record injection
wrong epoch transplantation
wrong device transplantation
public-anchor interval-0 forgery
```

---

## Loss recovery

A later disclosed key can recover earlier required chain values.

For `j > i`:

```text
K_(i+1) =
    F^(j-i)(
      K_(j+1)
    )
```

This permits verification despite loss of one or more intermediate KDR transmissions.

The repository tests deliberate KDR loss rather than assuming reliable evidence transport.

---

# Finality Receipts

A Finality Receipt records the protected execution-finality decision.

A representative chained construction is:

```text
R_n =
  Auth_K(
    Header_n ||
    B_n ||
    Counter_n ||
    H(R_(n-1))
  )
```

A receipt can bind:

```text
decision
Candidate Act / commitment
sink
context
policy generation
revocation generation
freshness
receipt counter
previous receipt digest
safe-state selection
```

The modeled ordering requires the receipt state to be committed before the execution capability becomes usable.

Conceptually:

```text
read current state
       |
consume freshness
       |
commit receipt
       |
release capability
       |
effectuate
```

Failure of the protected receipt or replay state in the high-assurance model causes denial rather than silent continuation.

---

# Bounded execution capability

Successful verification need not directly actuate hardware.

The protected boundary may instead issue a sink-local capability:

```text
E =
  MAC_KS(
    BindingCommitment ||
    SinkID ||
    ActuatorEnvelope ||
    Counter
  )
```

`K_S` is modeled as protected capability-authentication material unavailable to the ordinary proposing software.

The downstream actuator or protected sink accepts only an appropriately scoped capability.

This preserves a distinction between:

```text
verification succeeded
```

and:

```text
physical effect may now occur
```

---

# Atomic currentness and replay control

The harness tests races in which authority changes after an early validation.

A typical sequence is:

```text
early pre-check
    |
policy/revocation changes
    |
atomic consume begins
    |
read CURRENT policy / revocation
    |
mismatch detected
    |
DENY
```

The deciding generation read is modeled inside the final protected transition.

This is specifically intended to test the difference between:

```text
fresh observation
```

and:

```text
commit-time guarantee
```

---

# Spatial revalidation

The reference model includes a conservative boundary-proximity revalidation rule.

Stopping distance:

```text
s_stop(v_max) =
    v_max * tau
    +
    v_max^2 / (2 * a_brk)
```

where:

```text
v_max   maximum permitted outward speed
tau     enforcement-to-actuator reaction latency
a_brk   guaranteed deceleration
```

A sufficient revalidation constraint is:

```text
v_max * Delta_r
+
s_stop(v_max)
+
epsilon_pos
<=
d(t)
```

Therefore:

```text
Delta_r
<=
(
  d(t)
  -
  epsilon_pos
  -
  s_stop(v_max)
)
/ v_max
```

The included tests reproduce the illustrative boundary examples and verify that a non-positive result removes authority for additional outward motion.

The model may instead:

```text
reduce speed
hold position
select a Safe-State action
```

depending on the configured profile.

---

# Multi-source position consistency

The implementation also includes an illustrative consistency predicate for multiple position sources.

For position estimates `p_i` with uncertainty `sigma_i`:

```text
||p_i - p_j||
<=
k * (sigma_i + sigma_j)
```

A conservative position uncertainty can be modeled as:

```text
epsilon_pos =
    k * max_i(sigma_i)
```

The tests can require a minimum number:

```text
q_min >= 2
```

of sufficiently independent or partially independent agreeing sources.

Failure to obtain sufficient agreement removes authority for the spatially scoped act rather than creating new movement authority.

---

# DAA conflict-set-bound execution finality

The DAA profile tests whether a maneuver authorized from one traffic picture can still be admitted after that traffic picture changes.

A deterministic conflict-set commitment is modeled as:

```text
C_root =
  H(
    CanonicalSort(
      I_1 ||
      I_2 ||
      ... ||
      I_n
    )
  )
```

Illustrative closest-point-of-approach calculations include:

```text
t_CPA,j =
  clamp(
    -(r_j . v_j) / ||v_j||^2,
    0,
    T
  )

d_CPA,j =
  ||r_j + v_j * t_CPA,j||
```

For candidate maneuver `M`:

```text
m_j(M) =
  d_CPA,j(M)
  -
  (
    D_req,j
    +
    epsilon_j
  )
```

and:

```text
MultiIntruderSafe(M)
<=>
min_j m_j(M) >= 0
```

The important execution-finality property is not the illustrative motion equation itself.

It is that the admitted maneuver remains bound to:

```text
the conflict set
ownship state
relevant intruders
motion sink
Resolution Epoch
```

A newly appearing higher-risk intruder or superseded Resolution Epoch therefore forces re-evaluation.

---

# Emergency-scene temporary authority

The autonomous-vehicle cross-domain profile models bounded temporary authority for emergency scenes.

A representative scene commitment is:

```text
S_scene =
  H(
    IncidentID ||
    ScenePolygon ||
    LocalEvidenceDigest ||
    TemporaryControlDigest ||
    SceneEpoch
  )
```

Local corroboration may use:

```text
SceneCorroborated
<=>
sum_i v_i >= q
```

where `v_i` represents a protected validation result from an evidence source.

The red-team suite does not merely count messages.

It attempts to satisfy q-of-n using correlated or duplicated evidence.

Temporary authority is also constrained by:

```text
incident currentness
scene match
vehicle match
expiry
revocation
nonce state
bounded motion envelope
localization margin
hard safety predicate
```

Authority extinguishes when the relevant scene state no longer applies.

---

# Atomic control-authority handover

The handover model tests whether two otherwise valid controllers can simultaneously acquire ordinary authority over the same governed sink.

The central invariant is:

```text
for every sink s and time t:

number of effective ordinary controllers <= 1
```

A representative mathematical form is:

```text
forall s,e,t:

sum_c A(c,s,e,t) <= 1
```

The protected state includes:

```text
CurrentController[s]
CurrentEpoch[s]
CurrentEnvelope[s]
```

A command is accepted only when its controller and epoch match current protected state.

Conceptually:

```text
PREPARE
   |
   v
COMMIT new authority epoch
   |
   v
old controller becomes stale
   |
   v
ENABLE new controller
```

The harness injects crashes:

```text
before PREPARE completion
after PREPARE
during COMMIT
after epoch advance
before new controller ENABLE
after ENABLE
```

The expected property is safe recovery without dual ordinary authority.

The packaged deterministic campaign exercises thousands of seeded crash sequences.

---

# Concurrency and replay testing

A single-use nonce is tested under concurrent access.

Representative campaign:

```text
50 concurrent consumers
same Candidate Act
same nonce
```

Expected result:

```text
exactly one consume may succeed
all others fail replay / already-consumed checks
```

This is important because a sequential unit test alone does not exercise the race that actually matters.

---

# Fault injection

The repository defines explicit fault boundaries around the finality transition.

Representative checkpoints include:

```text
F0 before current-state read
F1 after current-state read
F2 after nonce reservation
F3 after replay consume
F4 during receipt construction
F5 after durable receipt commit
F6 after capability creation
F7 after sink acceptance but before modeled effect
```

Hardware implementations should extend this approach to:

```text
power interruption
watchdog reset
brownout
DMA interference
bus retry
secure-element timeout
flash-write interruption
cross-core reset
actuator-controller restart
```

The software harness does not claim to reproduce the physics of these hardware faults.

It provides a model for where such testing should occur.

---

# Test status

Run:

```bash
pytest
```

to obtain the authoritative local result.

The packaged snapshot includes:

```text
66 automated tests
```

covering ordinary and adversarial behavior.

The packaged reference campaign also includes:

```text
5,000 deterministic seeded
control-authority-handover crash schedules
```

with zero modeled dual-authority violations in that finite campaign.

These numbers must be interpreted narrowly.

They demonstrate the behavior of this reference model for the executed test set.

They do not constitute exhaustive proof.

---

# Test categories

Representative test families include:

```text
positive/
    expected valid execution paths

negative/
    malformed and semantically invalid inputs

replay/
    nonce and single-use enforcement

revocation_race/
    state changes between pre-check and commit

fragmentation/
    loss, corruption, duplication, mixing

aer/
    delayed-disclosure evidence attacks

daa/
    stale conflict sets and Resolution Epochs

emergency_scene/
    expired / correlated / stale scene authority

handover/
    crash, split-brain, stale-controller cases

concurrency/
    simultaneous consume attempts

fault_injection/
    crash points around protected commit
```

---

# Test vectors

The repository includes deterministic test vectors for exchangeable validation of:

```text
BPC generation
binding commitments
Authority References
fragment roots
fragment authenticators
AER generation
KDR disclosure
chain recovery
AER verification
receipt linkage
```

The intention is to make it possible for independent implementations to compare concrete byte-level results rather than relying only on prose descriptions.

---

# System variables

Security-relevant and timing-relevant assumptions are exposed in configuration files.

Representative BPC variables include:

```yaml
binding_bits: 64
authority_ref_bits: 32
tag_bits: 64

collision_domain_q: 100000
offline_work_budget_W: 1000000000
online_attempt_budget: 1000

target_collision_probability: 1e-9
target_substitution_probability: 1e-9
target_forgery_probability: 1e-9
```

Representative AER variables include:

```yaml
interval_seconds: 1
disclosure_delay_intervals: 3
observer_clock_uncertainty_ms: 500
chain_length: 4096
aer_tag_bits: 64
packet_loss_probability: 0.10
packet_reorder_probability: 0.02
```

Representative spatial variables include:

```yaml
distance_to_boundary_m: 60
position_uncertainty_m: 5
max_speed_mps: 15
reaction_latency_ms: 100
guaranteed_deceleration_mps2: 5
```

These values are illustrative deployment inputs, not universal safety parameters.

---

# Benchmarks

The repository contains a local software measurement harness.

Representative measurements include:

```text
BPC generation latency
BPC verification latency
AER generation latency
AER verification latency
nonce consume latency
receipt commit latency
fragment reconstruction latency
throughput
memory use
p50 latency
p95 latency
p99 latency
maximum observed latency
```

The environment report records, where available:

```text
CPU
architecture
RAM
operating system
Python version
cryptographic implementation
storage backend
test date
commit identifier
```

---

## Benchmark interpretation

The benchmark numbers are measurements of the **local reference implementation**.

They are not actuator-grade latency claims.

Unless specifically measured on a real target, they exclude:

```text
certified flight-control hardware
automotive safety MCU behavior
secure-element access latency
HSM latency
real radio propagation
CAN arbitration
Ethernet TSN scheduling
RTOS scheduling
DMA effects
cache interference
flash persistence delays
hardware watchdogs
physical actuator response
certification overhead
```

A high decisions-per-second number in an in-memory Python test therefore means only that the modeled cryptographic and state-machine path can execute at that measured rate in the reported software environment.

---

# Reference implementation versus production implementation

This repository deliberately separates:

```text
architectural plausibility
```

from:

```text
production assurance
```

A production implementation would additionally require, depending on domain:

```text
hardware-rooted key protection
protected boot and measurement
secure provisioning
trusted time
persistent anti-rollback state
real actuator gating
bus-path closure
alternate-path analysis
WCET analysis
fault-containment design
certification evidence
independent security review
penetration testing
physical attack evaluation
safety-case integration
```

The repository does not claim those steps have been completed.

---

# Interpretation boundaries

Passing this harness demonstrates that the **reference state machine and cryptographic bindings** satisfy the tested invariants under the modeled adversary.

It does not prove:

* aircraft airworthiness;
* automotive functional safety;
* certified Detect-and-Avoid safety;
* certified autonomous-driving safety;
* actuator hardware non-bypassability;
* absence of hidden alternate physical paths;
* secure-element tamper resistance;
* HSM assurance;
* TEE assurance;
* MCU fault containment;
* FPGA correctness;
* worst-case real-time execution;
* radio interoperability;
* RF coexistence;
* complete formal verification;
* universal cryptographic security;
* correctness against every possible attacker;
* correctness under every physical failure;
* regulatory compliance;
* aviation certification;
* automotive certification;
* production readiness;
* legal authorization of any act;
* that a verified AER proves the physical act occurred.

A verified AER means only that the modeled protected evidence mechanism authenticated the corresponding protected decision record under the tested construction.

---

# What a successful test does prove

A successful test has a narrower and more useful meaning.

For example:

```text
test_parameter_substitution
```

supports the statement:

> Under the modeled canonicalization, binding, key assumptions, and implementation path used by the test, changing a tested load-bearing parameter after authorization causes verification failure.

It does **not** support:

> Parameter substitution is impossible in every real aircraft.

Likewise:

```text
test_no_dual_controller
```

supports:

> No tested transition in the implemented handover model produced two simultaneously effective ordinary controllers under the tested schedules.

It does not establish that every production distributed-system implementation will preserve that property.

This distinction is intentional throughout the repository.

---

# Why negative tests matter

A conventional demo often establishes:

```text
valid input -> valid result
```

Execution-finality engineering requires substantially more:

```text
valid authority + modified act        -> DENY
valid authority + wrong sink          -> DENY
valid authority + stale epoch         -> DENY
valid authority + replay              -> DENY
valid evidence + too-late arrival     -> DISCARD
partial proof                         -> NON-EFFECTIVE
missing state                         -> UNKNOWN / DENY
receipt-store failure                 -> NO RELEASE
old controller                        -> DENY
safe action during authority failure  -> AVAILABLE
```

The repository therefore treats denial behavior as a primary implementation output rather than an error-path afterthought.

---

# Evidence is not authority

The repository enforces a deliberate separation between execution inputs and audit evidence.

The following are **not accepted as execution authority merely because they verify**:

```text
Finality Receipt
Act Evidence Record
Key Disclosure Record
Evidence Anchor
audit log
observer record
```

They provide evidence about protected decisions.

They do not themselves authorize a new physical act.

This rule prevents an audit artifact from accidentally becoming a bearer capability.

---

# Safe-state asymmetry

For cyber-physical systems, “fail closed” cannot always mean “freeze everything.”

Some actions may be necessary to reduce physical risk.

The architecture therefore distinguishes:

```text
permission-expanding act
```

from:

```text
pre-authorized safety-increasing act
```

Examples of a Safe-State Set may include:

```text
controlled braking
reduced speed
hover
loiter
controlled descent
landing
return-to-home
minimal-risk stop
payload lock
RF reduction
```

The exact safe actions are deployment-specific and must be defined by the applicable safety architecture.

The reference harness tests the important property that failure of fresh authority does not automatically remove every pre-authorized safety-reducing option.

---

# Reproducibility

To reproduce a result, record:

```text
repository commit
Python version
operating system
configuration file
random seed
test command
benchmark command
environment variables
```

Randomized campaigns use explicit seeds where possible so that a failing state sequence can be replayed.

A red-team failure should therefore be convertible into:

```text
seed
+
configuration
+
transition trace
+
expected invariant
+
observed violation
```

rather than remaining an unreproducible anecdote.

---

# Relationship to the Internet-Draft

The repository accompanies the execution-finality work described in the related UAS/autonomous-vehicle Internet-Draft.

The Internet-Draft describes:

```text
architecture
terminology
wire / object concepts
processing model
security properties
failure behavior
interoperability questions
```

The repository provides:

```text
executable interpretation
adversarial tests
test vectors
system variables
fault models
local measurements
```

The repository is informative engineering material.

It is not itself an IETF standard and does not create protocol requirements beyond the applicable specification text.

---

# Related architectural publication

Broader background on the execution-finality problem is available in:

**The Internet Solved Communication. It Never Solved Authority.**

Zenodo:

[https://zenodo.org/records/22082995](https://zenodo.org/records/22082995)

The central architectural distinction is:

> **Computation is not authority.**

A system can correctly compute an operation, authenticate a requester, validate a credential, and securely transport a command while still requiring a separate protected decision before that operation becomes externally effective.

---

# Public repository


Repository title:

**Execution Finality for UAS and Autonomous Vehicles — Act-Bound Authorization, Finality Sinks, and Verifiable Act Evidence**

---

# Questions for Reviewers 

Independent reviewers are encouraged to challenge the architecture with concrete counterexamples.

Useful questions include:

1. Can an alternative command path reach the actuator without crossing the modeled Finality Sink?
2. Is every load-bearing field included in canonicalization?
3. Can a valid proof be transplanted to another sink?
4. Can an authorization survive a relevant policy or revocation change?
5. Is freshness consumed atomically with final release?
6. Can a crash produce duplicate effectuation?
7. Can a receipt be lost after effectuation?
8. Can fragmented proof material be mixed across sessions?
9. Can a compact commitment be ambiguously resolved?
10. Can public delayed-disclosure material be abused to forge an earlier AER?
11. Is the observer timing condition conservative enough?
12. Can DAA authority survive a changed conflict set incorrectly?
13. Can a stale Resolution Epoch still reach motion admission?
14. Can two controllers become simultaneously effective during handover?
15. Can correlated evidence satisfy a q-of-n scene requirement?
16. Can failure of authority remove a necessary safety action?
17. Is an evidence artifact ever accepted as effectuation authority?
18. What protected state must survive reboot?
19. What happens when durable state is unavailable?
20. Which assumptions would fail when ported to real avionics or vehicle hardware?

Concrete failing traces and reproducible test cases are especially useful.

---

# Contributing adversarial cases

Useful contributions include:

```text
new negative test
new race condition
new crash point
new state-machine counterexample
alternate-path bypass case
new test vector
cross-language implementation
hardware timing result
real transport trace
formal model
proof attempt
cryptographic critique
canonicalization ambiguity
packet-loss scenario
counterexample to an invariant
```

A contribution that breaks an invariant is more valuable than a contribution that merely adds another happy-path demo.

---

# Security disclosure

If a finding concerns only the reference implementation, it may be reported through the repository's security process described in:

```text
SECURITY.md
```

If a finding appears to invalidate an architectural invariant rather than merely an implementation detail, the report should identify:

```text
affected invariant
assumptions
minimal reproducer
state transition
expected behavior
observed behavior
security consequence
```

This distinction helps separate:

```text
bug in this code
```

from:

```text
counterexample to the architecture
```

---

# License

Unless a file states otherwise, the copyrightable contents of this repository are licensed under:

**Creative Commons Attribution-NonCommercial 4.0 International — CC BY-NC 4.0**

Non-commercial sharing and adaptation are permitted subject to the license conditions, including attribution, license notice, and indication of changes.

See:

```text
LICENSE.md
```

---

# Patent-right separation

The copyright license does **not** itself grant:

```text
patent rights
SEP rights
FRAND rights
commercial patent rights
trademark rights
production rights
certification rights
```

No patent license should be inferred merely from access to the code, tests, documentation, diagrams, or repository.

See:

```text
IPR-NOTICE.md
```

for the applicable notice.

---

# Limitations

The full limitations statement is maintained in:

```text
LIMITATIONS.md
```

In particular, this repository does not establish:

```text
airworthiness
functional-safety certification
production security
regulatory compliance
formal correctness
hardware non-bypassability
complete threat coverage
universal cryptographic security
real-time guarantees
patent validity
patent infringement
freedom to operate
standard essentiality
```

Passing the test harness should therefore be interpreted as **evidence about this reference implementation under the tested assumptions**, not as a universal proof about every system implementing related ideas.

---

# Closing principle

The repository is built around a simple distinction:

```text
communication is not authority
authentication is not authority
computation is not authority
possession is not authority
evidence is not authority
```

For a consequence-bearing operation, authority becomes meaningful only when the actual pending act is checked at the boundary where it can still be prevented from becoming effective.

That boundary is the focus of this repository.


