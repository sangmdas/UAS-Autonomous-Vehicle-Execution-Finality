# Threat Model: UAS / Autonomous-Vehicle Execution Finality

This document defines the security boundaries, adversary capabilities, protected assumptions, attack surfaces, residual risks, and test mappings for the `UAS-Autonomous-Vehicle-Execution-Finality-Reference` repository.

The reference implementation is deliberately **red-team first**. It does not assume that an authenticated command, a privileged process, a valid token, or a successfully computed maneuver is entitled to produce a physical effect. The protected decision is made at the modeled effectuation boundary.

> **Core security rule:** computation, authentication, prior authorization, and possession of evidence are not, by themselves, effectuation authority.

The model asks whether a concrete pending act can remain non-effective until the protected boundary verifies the actual act, the intended sink, current authority state, freshness, context, and any profile-specific safety predicates.

---

## 1. Security Objective

For an ordinary consequence-bearing Candidate Act `A` directed to Finality Sink `S`, the principal modeled invariant is:

```text
NOT Verify(CurrentState, ActualPendingAct, S, Authority, Freshness)
    =>
NOT Effectuate(A)
```

The repository tests narrower properties that support this objective, including:

```text
changed act                 -> binding mismatch / deny
changed sink                -> sink mismatch / deny
consumed nonce              -> replay deny
stale policy generation     -> deny at final commit
stale revocation generation -> deny at final commit
missing fragment            -> incomplete / no authority
ambiguous proof             -> fail closed or escalate
receipt commit failure      -> no release
late AER                    -> discard
evidence object             -> never execution authority
stale DAA conflict set      -> motion admission deny
stale controller epoch      -> command deny
handover                    -> no dual ordinary authority
safe-state action           -> remains available where configured
```

The harness does **not** prove that every real aircraft or vehicle satisfies these invariants. It tests the implemented model under the stated assumptions.

---

## 2. Architectural Trust Boundaries

The model separates an untrusted act-proposing domain from the Protected Enforcement Domain (PED) and the Finality Sink.

```text
      UNTRUSTED / LESS-TRUSTED DOMAIN

  Mission computer / autonomy stack / AI planner
  Ground-control input / fleet service / network
  Caller-supplied objects / ordinary application state

                       |
                       | Candidate Act / authority input
                       v
================================================================
                    TRUST BOUNDARY
================================================================
                       |
                       v
        PROTECTED ENFORCEMENT DOMAIN (PED)

   protected keys
   current policy / revocation state
   nonce and replay state
   receipt state
   evidence key-chain state
   protected controller / epoch state

                       |
                       | bounded release / enablement
                       v
                FINALITY SINK

   ESC / motor gate / payload latch / RF gate
   sensor gate / trajectory admission / motion gate

                       |
                       v
                EXTERNAL EFFECT
```

The software reference model treats the PED and sink as logical security boundaries. A production system would need to realize those boundaries using platform-specific hardware, firmware, isolation, bus gating, secure storage, or other non-bypassable mechanisms.

---

## 3. Adversary Capabilities Exercised by the Harness

The modeled adversary may control or influence the untrusted side of the boundary and may attempt to:

- modify load-bearing Candidate Act parameters after authorization;
- substitute a different destination, trajectory, payload parameter, or context digest;
- redirect a valid proof to another sink;
- copy a valid proof to another session or device scope;
- replay a single-use act;
- race concurrent consumers against the same nonce;
- advance policy state after an early pre-check;
- advance revocation state before the final protected commit;
- cause protected receipt persistence to fail;
- delete, corrupt, duplicate, reorder, or cross-mix BPC fragments;
- present fragments authenticated under the wrong key;
- exploit the public AER anchor commitment to attempt an interval-0 forgery;
- inject a validly authenticated AER after the corresponding chain value has become public;
- suppress intermediate Key Disclosure Records;
- present a wrong KDR chain value;
- transplant evidence between device identities or evidence epochs;
- add a new DAA intruder after a maneuver has been authorized;
- reuse a superseded Resolution Epoch;
- present stale traffic state;
- satisfy a q-of-n emergency-scene rule with correlated observations;
- continue using temporary scene authority after expiry, scene exit, or revocation change;
- crash control-authority handover at PREPARE, COMMIT, or ENABLE boundaries;
- replay a command from an old Control Authority Epoch;
- violate a bounded control envelope.

The adversary is therefore stronger than an ordinary malformed-input client, but weaker than an attacker who has already physically bypassed the Finality Sink or extracted the protected root keys. Those latter cases violate protected assumptions and are treated separately below.

---

## 4. Protected Assumptions

The reference harness assumes the following properties for the modeled security claims to hold:

1. **Protected root and sink-local keys remain secret.** `K_root`, binding keys, BPC authentication keys, fragment keys, sink capability keys, and the AER master seed are not directly disclosed to the untrusted domain before their intended use or disclosure point.

2. **Cryptographic primitives behave as modeled.** SHA-256, HMAC-SHA-256, and the HKDF-style derivation used by the reference implementation are assumed to provide their expected cryptographic properties. The repository is not a formal proof of those primitives.

3. **The protected atomic section is not bypassed.** Current-state verification, replay consumption, receipt commitment, and capability release occur according to the modeled ordering.

4. **The Finality Sink is on the consequence path.** The protected effect cannot occur through an unmodeled alternate hardware, bus, DMA, debug, maintenance, firmware, or power path.

5. **Protected persistent state is not arbitrarily rolled back.** Where the model relies on monotonic counters, consumed nonces, receipt linkage, controller epochs, or revocation generations, production implementations must provide suitable persistence and rollback resistance.

6. **Trusted context inputs meet their stated assumptions.** The harness can test consistency and freshness rules, but it does not prove the physical integrity of GNSS, VIO, sensors, traffic surveillance, responder credentials, or external authority services.

7. **Safe-state definitions are supplied by the applicable safety architecture.** The harness models availability of configured safe actions; it does not determine that a particular maneuver is physically safe for every platform and environment.

---

## 5. Threat Matrix and Test Mapping

The table maps attack objectives to the concrete repository tests that exercise them. Test names refer to functions under `tests/` in the packaged repository.

| ID | Threat | Adversary objective / vector | Modeled mitigation | Representative tests |
|---|---|---|---|---|
| T-01 | Act substitution | Change a load-bearing parameter after authorization | Canonical Candidate Act digest plus keyed act binding; sink reconstructs actual pending act | `test_argument_substitution_denied`, `test_context_substitution_denied` |
| T-02 | Sink substitution | Reuse a valid proof at a different actuator or motion boundary | Sink identifier is part of the protected binding and sink-scoped derivation | `test_sink_substitution_denied`, `test_sink_scope_changes_binding_key`, `test_wrong_motion_sink_rejected` |
| T-03 | Replay | Re-execute a single-use act or race many consumers | Protected nonce / freshness consume before release | `test_replay_denied`, `test_50_way_same_nonce_concurrency_allows_exactly_once` |
| T-04 | Policy/revocation race | Pass an early pre-check and actuate after authority changed | Deciding generations are checked again at final protected commit | `test_policy_change_after_precheck_denied_at_commit`, `test_revocation_change_after_precheck_denied_at_commit` |
| T-05 | Receipt persistence failure | Effectuate while the evidence / replay transaction did not commit durably | Fail closed when receipt persistence fails | `test_receipt_store_failure_fails_closed`, `test_receipt_failure_retry_does_not_effectuate` |
| T-06 | Fragment confusion | Mix, omit, corrupt, duplicate, or cross-session BPC fragments | Session/root/index/count authentication and complete reconstruction before use | `test_missing_fragment_is_incomplete`, `test_mixed_session_rejected`, `test_corrupted_fragment_rejected`, `test_duplicate_index_rejected`, `test_wrong_key_rejected` |
| T-07 | Public-anchor AER forgery | Use public `K_0` to forge the first evidence interval | `K_0` is commitment only; interval `i` uses `K'_i = F'(K_(i+1))` | `test_public_k0_cannot_derive_interval0_valid_tag`, `test_master_seed_is_distinct_from_terminal_chain_value`, `test_tag_key_not_chain_member` |
| T-08 | Post-disclosure evidence forgery | Forge an old AER after its chain value has become public | Observer timing / late-record rejection | `test_late_record_rejected_even_if_tag_valid` |
| T-09 | Evidence transplantation / disclosure loss | Move evidence across device/epoch or exploit dropped KDRs | Device and epoch binding; reverse-chain loss recovery | `test_wrong_epoch_record_rejected`, `test_wrong_device_record_rejected`, `test_wrong_kdr_key_rejected`, `test_loss_of_intermediate_kdr_recovered_by_later_disclosure` |
| T-10 | DAA stale-basis admission | Admit a maneuver after the relevant traffic picture or Resolution Epoch changed | Conflict-set continuity, current track freshness, sink binding, monotonic Resolution Epoch | `test_new_intruder_invalidates_old_resolution`, `test_stale_resolution_epoch_rejected`, `test_stale_track_fails_closed`, `test_multi_intruder_one_unsafe_means_whole_maneuver_unsafe` |
| T-11 | Correlated emergency evidence | Satisfy q-of-n using multiple reports derived from one underlying source, or reuse expired scene authority | Source deduplication / independence semantics, vehicle/scene/expiry/revocation binding, hard-safety predicate | `test_two_channels_same_physical_source_count_once`, `test_wrong_vehicle_denied`, `test_scene_exit_denied`, `test_expiry_denied`, `test_revocation_epoch_change_denied`, `test_hard_safety_failure_denied` |
| T-12 | Split-brain control | Allow two controllers or an old controller to retain effect authority during/after handover | Protected `CurrentController`, monotonic `CurrentEpoch`, PREPARE/COMMIT/ENABLE state machine | `test_prepare_does_not_enable_new_controller`, `test_commit_creates_safe_only_gap_not_dual_authority`, `test_enable_switches_exclusively_to_new_controller`, `test_crash_injection_never_yields_dual_authority`, `test_old_epoch_rejected_after_complete_handover`, `test_randomized_handover_sequences_preserve_exclusivity` |
| T-13 | Spatial-boundary overrun | Continue outward motion when the authority revalidation margin is exhausted | Boundary-distance, uncertainty, latency, speed, and guaranteed-deceleration bound | `test_worked_example_60m`, `test_worked_example_30m`, `test_speed_reduction_restores_margin`, `test_nonpositive_interval_requires_hold_or_safe_action` |
| T-14 | Position-source inconsistency | Treat conflicting location estimates as sufficient context | Minimum-source and uncertainty-dependent consistency predicate | `test_two_consistent_sources_pass`, `test_insufficient_consistent_sources_fail` |
| T-15 | Unsafe fail-closed interpretation | Remove braking / minimal-risk action merely because ordinary authority fails | Separate pre-authorized Safe-State Set | `test_brake_remains_available_when_ordinary_authority_fails`, `test_permission_expansion_not_safe_by_default` |
| T-16 | Compact-binding under-sizing | Treat a short truncated value as automatically secure | Explicit collision and attacker-work sizing | `test_collision_formula_and_inverse_are_consistent`, `test_offline_substitution_formula_and_inverse_are_consistent`, `test_64_bits_not_automatically_safe_for_large_offline_budget` |

---

## 6. Detailed Threat Classes

### 6.1 Act and Parameter Substitution

The attacker obtains or observes authorization for act `A` and changes a load-bearing field before effectuation, producing `A'`.

Representative examples:

```text
authorized drop-zone D1 -> attempted D2
authorized corridor C7  -> attempted C8
authorized camera area  -> changed area
authorized speed bound  -> enlarged speed bound
```

The modeled defense is not merely signature verification. The binding is recomputed over the actual pending act and compared at the sink.

Residual risk: if a materially effect-determining field is omitted from canonicalization, the binding cannot protect that field. Canonicalization completeness is therefore a security property and must be reviewed per act class.

### 6.2 Sink Substitution

A proof intended for one consequence boundary is presented to another.

The model binds `SinkID` into the commitment and uses sink-scoped key derivation where configured. This prevents a proof for one actuator class from becoming a generic bearer capability.

Residual risk: two physically distinct paths accidentally configured with the same sink identity or shared capability key can defeat this separation. Production provisioning must preserve sink uniqueness or explicitly defined sink classes.

### 6.3 Replay and Concurrency

The attacker reuses a single-use proof or races many simultaneous consumers.

The model expects exactly one successful consume of a protected nonce/freshness value. A sequential replay test is not sufficient; the repository includes a concurrent same-nonce test.

Residual risk: production persistence and multi-core synchronization must provide the same atomicity. An in-memory Python lock does not demonstrate MCU, database, secure-element, or distributed-store atomicity.

### 6.4 Currentness Race

An operation passes an early policy or revocation check, but policy state changes before release.

The deciding state is therefore read inside the modeled final protected commit. Early reads are treated only as pre-checks.

Residual risk: a production system must define what source is authoritative, how updates become visible to the PED, and what atomicity means when the authority state is maintained outside the same hardware boundary.

### 6.5 Fragmentation Attacks

A constrained link may carry a BPC across multiple fragments. The attacker may omit, duplicate, corrupt, reorder, or cross-mix fragments.

The model requires authenticated membership in one session/root/count set and complete reconstruction before the proof is usable.

Residual risk: denial of service remains possible by dropping required fragments. The security goal is to prevent partial evidence from becoming authority, not to guarantee availability over a hostile channel.

### 6.6 Delayed-Disclosure AER Attacks

The evidence construction separates a never-disclosed master seed from discloseable reverse-chain values:

```text
K_seed := protected master seed; never disclosed
K_N    := Trunc_128(H("UAS-AFE-seed" || K_seed || EpochID))
K_i    := F(K_(i+1))
K'_i   := F'(K_(i+1))
K_0    := public chain commitment only
```

Threats include:

- deriving an interval-0 tag key from public `K_0`;
- forging a record after `K_(i+1)` becomes public;
- transplanting a record across `DeviceID` or `EpochID`;
- suppressing KDR messages;
- injecting a false disclosed chain value.

The observer safety rule and reverse-chain recovery logic are exercised explicitly.

Residual risk: a verified AER is evidence that the modeled protected domain authenticated a decision record. It is **not** independent proof that the corresponding physical act actually occurred.

### 6.7 DAA Basis Substitution

A DAA maneuver can become unsafe or irrelevant if the conflict set changes after computation. The threat is not only a forged command; it is a once-valid resolution used against a different current traffic basis.

The model therefore ties admission to the current conflict-set state, track freshness, motion sink, and Resolution Epoch.

Residual risk: the reference model does not certify surveillance integrity, sensor fusion, well-clear thresholds, aircraft dynamics, or regulatory DAA compliance. It tests state continuity around a simplified maneuver-admission model.

### 6.8 Emergency-Scene Correlation

Multiple messages do not necessarily represent multiple independent observations. The red-team harness models q-of-n corroboration with source identity so two channels derived from the same physical source do not automatically count twice.

Residual risk: determining real-world independence among sensors, responders, infrastructure feeds, and network paths is deployment-specific and may be difficult. The software model cannot prove independence of physical evidence.

### 6.9 Control-Authority Split Brain

Two individually legitimate controllers may both believe they possess control authority during a handover or crash recovery.

The modeled handover uses protected controller state and a monotonic Control Authority Epoch. PREPARE does not give the new controller authority; COMMIT can produce a safe-only gap; ENABLE activates the new controller only under the new epoch.

Residual risk: the reference state machine assumes the governed sink obeys the protected epoch state. A production implementation must prevent stale controllers from reaching an alternate actuation path.

---

## 7. Physical and Integration Threats Not Proven by the Harness

The most important boundary of this repository is **path completeness**.

The Python harness cannot prove that every physical or firmware route to an actuator is actually gated by the PED. A real system can invalidate the model if any bypass exists, including for example:

- direct DMA into actuator-facing registers;
- debug or maintenance interfaces;
- bootloader or recovery-mode writes;
- secondary CAN / Ethernet / avionics bus paths;
- redundant controllers not governed by the same protected state;
- power-stage or gate-driver override lines;
- compromised firmware below the modeled sink;
- unsafe fallback modes;
- direct RF or sensor enable paths;
- manufacturing or service interfaces;
- physical tampering.

A production claim of non-bypassability therefore requires platform-specific path enumeration, hardware review, fault injection, and ideally independent assurance.

---

## 8. Availability and Safe-State Risks

Fail-closed behavior can itself be hazardous in cyber-physical systems. The model therefore distinguishes ordinary permission-expanding acts from a configured Safe-State Set.

Possible safe actions can include, depending on the platform:

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

The harness verifies only the **authority semantics** around these configured actions. It does not establish that a particular safe-state maneuver is aerodynamically, mechanically, or operationally safe in a real environment.

---

## 9. Context-Integrity Residual Risk

Execution finality can check the context it is given; it cannot create trustworthy physical truth from compromised sensors.

Examples of residual context risk include:

- coordinated GNSS spoofing;
- systematic VIO or map error;
- compromised external traffic data;
- stale but internally consistent sensor fusion;
- false emergency-scene evidence;
- clock corruption outside the protected time assumption;
- authority-service compromise.

Multi-source consistency and q-of-n rules reduce some classes of single-source failure but do not prove that all sources are independent or truthful.

---

## 10. Cryptographic and Key-Management Residual Risk

The harness uses conventional cryptographic primitives and explicit domain separation, but it is not a formal cryptographic proof or a production key-management system.

A production system must additionally address:

- root-key provisioning;
- hardware-backed key storage;
- key rotation;
- compromise recovery;
- secure deletion;
- device replacement;
- evidence-epoch rollover;
- entropy quality;
- side channels;
- rollback resistance;
- multi-tenant separation;
- secure time;
- certificate and issuer lifecycle where public-key objects are used.

The repository's key-separation tests demonstrate the intended reference behavior only.

---

## 11. Fault and Crash Model

The repository injects logical crashes around handover and finality-state transitions. A hardware implementation should extend fault injection to at least:

```text
power loss
brownout
watchdog reset
flash-write interruption
secure-element timeout
cross-core reset
bus retry / duplication
DMA interference
actuator-controller restart
network partition
clock discontinuity
```

Important checkpoints include:

```text
before current-state read
after current-state read
after nonce reservation
after replay-state consume
during receipt construction
after durable receipt commit
after capability generation
after sink acceptance but before physical effect
```

The software harness identifies where those tests matter; it does not reproduce their physical timing or electrical behavior.

---

## 12. Explicit Non-Claims

Passing this repository's tests does **not** establish:

- aircraft airworthiness;
- automotive functional-safety certification;
- certified Detect-and-Avoid safety;
- certified autonomous-driving safety;
- real actuator-path non-bypassability;
- secure-element, HSM, TEE, MCU, or FPGA assurance;
- worst-case execution time;
- deterministic real-time scheduling;
- RF interoperability or coexistence;
- full formal verification;
- exhaustive threat coverage;
- correctness under every physical or distributed-system failure;
- production key-management security;
- regulatory compliance;
- legal authority for any real-world act;
- production readiness;
- absence of vulnerabilities in any third-party product;
- that any named vendor implements or endorses this architecture;
- patent validity, infringement, novelty, inventive step, freedom to operate, or standard essentiality.

A passing test has the narrower meaning that the **reference implementation satisfied the tested invariant under the modeled assumptions and inputs**.

---

## 13. What Would Falsify the Architecture or Model

The repository is intended to invite counterexamples. Particularly valuable findings include a reproducible case where:

- a materially different Candidate Act passes an unchanged binding;
- a valid proof can be moved to an unintended sink;
- the same single-use nonce produces two effective releases;
- stale authority survives the final protected currentness check;
- incomplete or cross-session fragments become executable authority;
- public AER material permits a record to appear pre-disclosure when it was not;
- a superseded DAA Resolution Epoch is admitted;
- two controllers obtain simultaneous ordinary authority over one governed sink;
- an evidence artifact is accepted as execution authority;
- loss of ordinary authority also removes a required configured safe-state action;
- a modeled alternate path reaches the effect without passing the Finality Sink.

A failing trace should ideally include:

```text
repository commit
configuration
random seed, if applicable
state-transition trace
expected invariant
observed violation
minimal reproducer
```

---

## 14. Relationship to Other Repository Documents

Read this file together with:

- `ARCHITECTURE.md` — modeled execution-finality structure;
- `RED-TEAM-MODE.md` — adversarial campaign methodology;
- `FAULT-INJECTION.md` — crash and hardware-port fault boundaries;
- `SYSTEM-VARIABLES.md` — explicit modeled parameters;
- `TEST-MATRIX.md` — invariant-to-test traceability;
- `BENCHMARKS.md` — measurement methodology and interpretation;
- `LIMITATIONS.md` — complete non-claims and interpretation boundaries;
- `SECURITY.md` — reporting security findings;
- `IPR-NOTICE.md` — copyright/patent-right separation.

---

## 15. Closing Security Principle

The threat model is deliberately built around the distinction:

```text
identity       != effect authority
authentication != effect authority
computation    != effect authority
possession     != effect authority
evidence       != effect authority
```

For an ordinary consequence-bearing action, the protected boundary must still determine whether the **actual pending act** is permitted to become effective under the **current protected state**.
