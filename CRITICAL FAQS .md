# FAQ - UAS / Autonomous-Vehicle Execution Finality

*Questions from standards reviewers, safety engineers, cryptographic reviewers, avionics engineers, autonomous-vehicle engineers, and red-team reviewers.*

**Sangam Das** · Independent Inventor · info@sangamdas.com · 2026-09-18

> Computation, authentication, or possession of a token does not by itself create authority to make a consequential act effective.

The answers are intentionally conservative. They distinguish what the reference model demonstrates from what a production deployment would still need to prove.

*Status: Informational companion material to an individual IETF Internet-Draft. Not a working-group product.*

## Resources

- **Reference implementation and red-team harness** — https://github.com/sangmdas/UAS-Autonomous-Vehicle-Execution-Finality
- **IETF Internet-Draft** — https://datatracker.ietf.org/doc/draft-das-drip-uas-act-finality/
- **Architectural background** — https://zenodo.org/records/22082995
- **Machine-readable version of this FAQ** — `faq.json` (schema version 1.1)

## Scope

**In scope**

- Civil UAS in the specific and certified categories and comparable national regimes
- Civil autonomous road vehicles and other autonomous motion platforms
- Reference model and adversarial test harness for selected execution-finality invariants

**Out of scope**

- Weapons, weapon release, targeting, and counter-UAS engagement
- Airworthiness and certification requirements
- Replacement of flight-control safety design or automotive safety controllers
- Definition of legal rules or of which acts a regulator permits

## Contents (93 questions)

**Architecture Principles**

- [50. Why is "evidence is not authority" emphasized?](#50-why-is-evidence-is-not-authority-emphasized)
- [60. What is the core principle in one sentence?](#60-what-is-the-core-principle-in-one-sentence)
- [93. Does this architecture apply beyond drones and road vehicles?](#93-does-this-architecture-apply-beyond-drones-and-road-vehicles)

**Authority Lifecycle & Revocation**

- [15. What happens when a high-rate trajectory envelope is revoked?](#15-what-happens-when-a-high-rate-trajectory-envelope-is-revoked)
- [16. Does a revocation instantly remove every control output?](#16-does-a-revocation-instantly-remove-every-control-output)
- [17. How is TOCTOU handled between an early authorization check and effectuation?](#17-how-is-toctou-handled-between-an-early-authorization-check-and-effectuation)
- [18. What if revocation changes one microsecond after the atomic commit?](#18-what-if-revocation-changes-one-microsecond-after-the-atomic-commit)
- [19. What prevents replay of a valid execution handle?](#19-what-prevents-replay-of-a-valid-execution-handle)

**Binding & Path Completeness**

- [20. Why is the sink binding necessary if the act is already signed?](#20-why-is-the-sink-binding-necessary-if-the-act-is-already-signed)
- [21. What if an attacker finds an alternate path around the Finality Sink?](#21-what-if-an-attacker-finds-an-alternate-path-around-the-finality-sink)
- [22. Does the repository prove hardware non-bypassability?](#22-does-the-repository-prove-hardware-non-bypassability)
- [80. Does a manual remote-pilot or RC override path bypass the boundary?](#80-does-a-manual-remote-pilot-or-rc-override-path-bypass-the-boundary)
- [81. How are maintenance, bench-test, and firmware-update modes handled?](#81-how-are-maintenance-bench-test-and-firmware-update-modes-handled)

**Broadcast Act Evidence**

- [23. Does a valid AER prove that the physical act occurred?](#23-does-a-valid-aer-prove-that-the-physical-act-occurred)
- [24. Why use delayed disclosure for AER/KDR instead of signing every act?](#24-why-use-delayed-disclosure-for-aer-kdr-instead-of-signing-every-act)
- [25. Can the public chain anchor be used to forge interval 0?](#25-can-the-public-chain-anchor-be-used-to-forge-interval-0)
- [26. What if one or more KDR disclosures are lost?](#26-what-if-one-or-more-kdr-disclosures-are-lost)
- [27. How much clock synchronization does delayed disclosure require?](#27-how-much-clock-synchronization-does-delayed-disclosure-require)

**Claims & Falsifiability**

- [56. What is the strongest claim this repository can responsibly make?](#56-what-is-the-strongest-claim-this-repository-can-responsibly-make)
- [57. What would falsify the architecture rather than merely expose an implementation bug?](#57-what-would-falsify-the-architecture-rather-than-merely-expose-an-implementation-bug)

**Comparison With Existing Mechanisms**

- [14. Why not simply use CAN authentication or a MAC on the command?](#14-why-not-simply-use-can-authentication-or-a-mac-on-the-command)
- [36. Why not rely only on remote attestation?](#36-why-not-rely-only-on-remote-attestation)
- [37. Why not rely only on OAuth, signed commands, certificates, or ACLs?](#37-why-not-rely-only-on-oauth-signed-commands-certificates-or-acls)
- [84. Why not use a blockchain or distributed ledger for receipts and authority?](#84-why-not-use-a-blockchain-or-distributed-ledger-for-receipts-and-authority)

**Constrained Implementation**

- [11. How much memory does deterministic encoding and BPC verification require on a small MCU?](#11-how-much-memory-does-deterministic-encoding-and-bpc-verification-require-on-a-small-mcu)
- [12. Must every Finality Sink parse CBOR?](#12-must-every-finality-sink-parse-cbor)
- [13. Can the BPC fit inside an 8-byte CAN frame?](#13-can-the-bpc-fit-inside-an-8-byte-can-frame)
- [86. What is the energy and bandwidth overhead on a battery-powered platform?](#86-what-is-the-energy-and-bandwidth-overhead-on-a-battery-powered-platform)

**Context & Sensors**

- [8. Does spatial finality require GNSS + VIO + odometry in every vehicle?](#8-does-spatial-finality-require-gnss-vio-odometry-in-every-vehicle)
- [9. What if one localization source becomes unavailable or degraded?](#9-what-if-one-localization-source-becomes-unavailable-or-degraded)
- [10. Could strict multi-source agreement become a denial-of-service vector?](#10-could-strict-multi-source-agreement-become-a-denial-of-service-vector)

**Control Authority Handover**

- [47. How is control-authority handover protected against split brain?](#47-how-is-control-authority-handover-protected-against-split-brain)
- [48. What happens if the new controller crashes after the old controller is revoked?](#48-what-happens-if-the-new-controller-crashes-after-the-old-controller-is-revoked)
- [49. Does the repository prove the handover protocol for all distributed-system failures?](#49-does-the-repository-prove-the-handover-protocol-for-all-distributed-system-failures)

**Control Integration & Safety**

- [1. Does execution finality sit inside the flight-control or drive-by-wire inner loop?](#1-does-execution-finality-sit-inside-the-flight-control-or-drive-by-wire-inner-loop)
- [2. What is the exact latency overhead on a low-power microcontroller?](#2-what-is-the-exact-latency-overhead-on-a-low-power-microcontroller)
- [3. Could the finality layer destabilize an aircraft or vehicle if authorization becomes unavailable?](#3-could-the-finality-layer-destabilize-an-aircraft-or-vehicle-if-authorization-becomes-unavailable)
- [4. What happens if a coordinated multi-aircraft decision log becomes unreachable?](#4-what-happens-if-a-coordinated-multi-aircraft-decision-log-becomes-unreachable)
- [5. Is this safety-over-liveness design too conservative?](#5-is-this-safety-over-liveness-design-too-conservative)

**Deployment & Scope**

- [51. Can the architecture support existing autopilots and drive-by-wire systems without replacing them?](#51-can-the-architecture-support-existing-autopilots-and-drive-by-wire-systems-without-replacing-them)
- [52. Does the architecture require a new hardware chip?](#52-does-the-architecture-require-a-new-hardware-chip)
- [53. Is this an IETF protocol, a hardware architecture, or both?](#53-is-this-an-ietf-protocol-a-hardware-architecture-or-both)
- [87. What is the retrofit story? Can this be added to an existing airframe or vehicle?](#87-what-is-the-retrofit-story-can-this-be-added-to-an-existing-airframe-or-vehicle)
- [88. How does this work in multi-tenant fleets, where manufacturer, operator, and customer all have some authority?](#88-how-does-this-work-in-multi-tenant-fleets-where-manufacturer-operator-and-customer-all-have-some-authority)
- [89. Does any of this apply to weapons, targeting, or counter-UAS?](#89-does-any-of-this-apply-to-weapons-targeting-or-counter-uas)

**Detect & Avoid**

- [31. How does the design handle DAA traffic that changes after a maneuver was computed?](#31-how-does-the-design-handle-daa-traffic-that-changes-after-a-maneuver-was-computed)
- [32. Could DAA revalidation cause oscillation or repeated denial?](#32-could-daa-revalidation-cause-oscillation-or-repeated-denial)

**Drip & Remote Id**

- [68. What does an Observer actually gain, beyond what DRIP authentication already provides today?](#68-what-does-an-observer-actually-gain-beyond-what-drip-authentication-already-provides-today)
- [69. Why not simply sign act evidence with the DET key?](#69-why-not-simply-sign-act-evidence-with-the-det-key)
- [70. Does this require a new ASTM F3411 or ICAO carriage code point?](#70-does-this-require-a-new-astm-f3411-or-icao-carriage-code-point)

**Emergency Scene Profile**

- [33. How is q-of-n emergency-scene corroboration protected against correlated sensors?](#33-how-is-q-of-n-emergency-scene-corroboration-protected-against-correlated-sensors)

**Encoding Canonicalization Truncation**

- [43. Is deterministic CBOR mandatory?](#43-is-deterministic-cbor-mandatory)
- [44. What happens when two semantically equivalent encodings produce different bytes?](#44-what-happens-when-two-semantically-equivalent-encodings-produce-different-bytes)
- [45. What if a compact truncated binding collides?](#45-what-if-a-compact-truncated-binding-collides)
- [46. Why not simply use a full 256-bit digest everywhere?](#46-why-not-simply-use-a-full-256-bit-digest-everywhere)

**Evidence & Audit**

- [85. How do Finality Receipts relate to later audit, insurance claims, and investigation?](#85-how-do-finality-receipts-relate-to-later-audit-insurance-claims-and-investigation)

**Keys & Trust**

- [77. Who issues authority objects, and how is trust bootstrapped?](#77-who-issues-authority-objects-and-how-is-trust-bootstrapped)
- [78. How are evidence keys rotated, and what happens when a key chain is exhausted?](#78-how-are-evidence-keys-rotated-and-what-happens-when-a-key-chain-is-exhausted)

**Licensing & Ipr**

- [92. Is the architecture patented? What is the licensing posture?](#92-is-the-architecture-patented-what-is-the-licensing-posture)

**Offline Operation & Availability**

- [38. Does the architecture require a trusted centralized authority online for every act?](#38-does-the-architecture-require-a-trusted-centralized-authority-online-for-every-act)
- [39. What is the maximum offline window?](#39-what-is-the-maximum-offline-window)
- [40. Does fail-closed create a denial-of-service vulnerability?](#40-does-fail-closed-create-a-denial-of-service-vulnerability)

**Privacy & Transparency**

- [6. Does "privacy mode" defeat the transparency purpose of Act Evidence Records?](#6-does-privacy-mode-defeat-the-transparency-purpose-of-act-evidence-records)
- [7. If observers cannot see the exact camera activation event, what is being audited?](#7-if-observers-cannot-see-the-exact-camera-activation-event-what-is-being-audited)
- [76. What are the data-protection implications of broadcasting per-act evidence over a populated area?](#76-what-are-the-data-protection-implications-of-broadcasting-per-act-evidence-over-a-populated-area)

**Protected State & Failure**

- [28. What happens if the protected receipt store fails?](#28-what-happens-if-the-protected-receipt-store-fails)
- [29. Could receipt persistence itself become a denial-of-service target?](#29-could-receipt-persistence-itself-become-a-denial-of-service-target)
- [30. Why distinguish UNKNOWN from EMPTY?](#30-why-distinguish-unknown-from-empty)

**Regulatory**

- [73. Does implementing this make an operator compliant with Part 107, U-space, or EASA rules?](#73-does-implementing-this-make-an-operator-compliant-with-part-107-u-space-or-easa-rules)
- [74. How does this relate to certification standards such as DO-178C, DO-254, ISO 26262, ISO 21448, and UL 4600?](#74-how-does-this-relate-to-certification-standards-such-as-do-178c-do-254-iso-26262-iso-21448-and-ul-4600)
- [75. Is there any relationship to the EU AI Act, product liability, or accident investigation?](#75-is-there-any-relationship-to-the-eu-ai-act-product-liability-or-accident-investigation)

**Review & Resources**

- [58. What type of external review is most useful?](#58-what-type-of-external-review-is-most-useful)
- [59. Where are the public technical materials?](#59-where-are-the-public-technical-materials)
- [90. Are there test vectors, and how would two independent implementations be checked against each other?](#90-are-there-test-vectors-and-how-would-two-independent-implementations-be-checked-against-each-other)
- [91. How should a security issue or a counterexample be reported?](#91-how-should-a-security-issue-or-a-counterexample-be-reported)

**Robustness & Attack Surface**

- [41. Can a malicious planner spam the PED with verification requests?](#41-can-a-malicious-planner-spam-the-ped-with-verification-requests)
- [42. What prevents a large Candidate Act from becoming a parser attack surface?](#42-what-prevents-a-large-candidate-act-from-becoming-a-parser-attack-surface)

**Standards Process**

- [71. Is this a DRIP Working Group work item?](#71-is-this-a-drip-working-group-work-item)
- [72. What is the current status of the draft and the reference implementation?](#72-what-is-the-current-status-of-the-draft-and-the-reference-implementation)

**Standards Relevance**

- [54. Why is this relevant to RATS?](#54-why-is-this-relevant-to-rats)
- [55. Why is this relevant to COSE / CBOR?](#55-why-is-this-relevant-to-cose-cbor)

**Terminology**

- [61. What is a Candidate Act?](#61-what-is-a-candidate-act)
- [62. What is the Protected Enforcement Domain (PED)?](#62-what-is-the-protected-enforcement-domain-ped)
- [63. What is an Execution Handle, and why is it not a bearer token?](#63-what-is-an-execution-handle-and-why-is-it-not-a-bearer-token)
- [64. What is a Finality Sink and a withheld enablement condition?](#64-what-is-a-finality-sink-and-a-withheld-enablement-condition)
- [65. What is the difference between a BPC and an AER? They both look like compact proofs.](#65-what-is-the-difference-between-a-bpc-and-an-aer-they-both-look-like-compact-proofs)

**Threat Model & Residual Risk**

- [34. What if all context sensors are consistently wrong?](#34-what-if-all-context-sensors-are-consistently-wrong)
- [35. What if the PED itself is compromised?](#35-what-if-the-ped-itself-is-compromised)
- [79. What if GNSS time or position is spoofed?](#79-what-if-gnss-time-or-position-is-spoofed)
- [82. Could this become a remote kill switch, or a tool for grounding fleets?](#82-could-this-become-a-remote-kill-switch-or-a-tool-for-grounding-fleets)
- [83. What stops an operator from configuring the enforcement domain to allow everything?](#83-what-stops-an-operator-from-configuring-the-enforcement-domain-to-allow-everything)

**Uas Profile**

- [66. Which act classes does the UAS profile define, and why those?](#66-which-act-classes-does-the-uas-profile-define-and-why-those)
- [67. Why is RID_CHANGE treated as hostile to the operator?](#67-why-is-rid-change-treated-as-hostile-to-the-operator)

---

## Questions and Answers

### 1. Does execution finality sit inside the flight-control or drive-by-wire inner loop?

`control-integration-and-safety`

Not necessarily, and usually it should not.

The architecture is intended to separate: high-rate stabilization or control loops; lower-rate authorization, policy, and envelope decisions; and the final consequence-bearing boundary.

A 200-1000 Hz stabilization loop should not be forced to perform a full cryptographic authorization transaction for every control tick.

Instead, the preferred pattern is: slow / medium-rate authority decision -> protected verification -> bounded execution envelope / handle -> high-rate local control within that envelope.

The high-rate controller can continue operating locally as long as the current act remains inside the already verified envelope. Revalidation is required when the envelope expires, a protected generation changes, the act leaves the permitted range, or another load-bearing condition changes.

The reference architecture therefore distinguishes per-act finality from pre-authorized high-rate envelope execution.

A production system must still measure worst-case execution time on the target MCU/SoC/FPGA and demonstrate that the selected enforcement placement does not violate control-loop deadlines.

---

### 2. What is the exact latency overhead on a low-power microcontroller?

`control-integration-and-safety`

The repository does not claim a universal microsecond figure.

The correct answer depends on processor architecture, clock rate, hardware crypto support, memory hierarchy, persistent-state mechanism, secure-element latency, serialization format, transport framing, number of protected lookups, receipt persistence method, and whether the decision is a cold-path authorization or a hot-path envelope check.

The reference implementation measures software-path latency only. Those measurements are useful for relative engineering comparison, but they are not a substitute for target-hardware WCET analysis.

A production implementation should report at minimum: T_verify = T_parse + T_lookup + T_hash + T_MAC + T_replay + T_current_state + T_receipt_commit + T_compare, and separately report worst-case and percentile results for the actual deployment hardware.

---

### 3. Could the finality layer destabilize an aircraft or vehicle if authorization becomes unavailable?

`control-integration-and-safety`

A correct deployment should not translate "authority unavailable" into "physically freeze the vehicle."

The architecture distinguishes permission-expanding acts from a pre-authorized Safe-State Set. Examples may include hover, loiter, controlled braking, minimal-risk stop, controlled descent, return-to-home, reduced-speed mode, payload lock, or another platform-defined safety action.

The exact Safe-State Set is not defined universally by this repository. It must be supplied by the platform safety architecture.

The intended rule is: loss of fresh authority must not silently expand authority, but it also must not remove a separately pre-authorized safety action that is required to reduce physical risk.

---

### 4. What happens if a coordinated multi-aircraft decision log becomes unreachable?

`control-integration-and-safety`

Silence must not be interpreted as approval.

However, "no commit on silence" does not require an unsafe stationary HOLD. A deployment may define a bounded offline or degraded-mode policy: coordinated authority unavailable -> do not accept new coordinated expansion -> retain only the previously authorized safe envelope -> execute local deconfliction, loiter, return, or landing.

The important invariant is that loss of the coordination log cannot create new authority.

Liveness is handled by the Safe-State Set, bounded residual authority, local collision-avoidance rules, and deployment-specific degraded-mode policy, not by converting missing authorization into permission.

---

### 5. Is this safety-over-liveness design too conservative?

`control-integration-and-safety`

The architecture is deliberately conservative at the authority boundary, but it does not require the physical controller to stop functioning.

The design separates two questions: may the system perform a new consequence-expanding act, and what safety-preserving behavior remains permitted if the answer is no?

A deployment that simply freezes an aircraft or vehicle in a hazardous environment would be poorly designed even if its authorization logic were cryptographically correct.

Execution finality is therefore intended to be composed with, not replace, the platform's safety controller and minimal-risk behavior.

---

### 6. Does "privacy mode" defeat the transparency purpose of Act Evidence Records?

`privacy-and-transparency`

It can, if designed carelessly.

The purpose of an UNSPECIFIED or privacy-preserving act class is not to hide whether a protected decision occurred. It is to avoid broadcasting more sensitive operational detail than is necessary.

A privacy-preserving record can still expose that a protected decision occurred, the decision class, the relevant device or epoch binding, timing information within the permitted granularity, an act commitment, a sink or sink-class commitment, and later-verifiable authenticity.

A privacy profile should therefore distinguish publicly verifiable decision evidence from public disclosure of every act parameter.

Where a regulator, auditor, or authorized investigator requires full detail, the deployment may retain a protected local receipt or selectively disclose the committed act under the applicable legal process.

The repository does not claim that one privacy profile is appropriate for all jurisdictions.

---

### 7. If observers cannot see the exact camera activation event, what is being audited?

`privacy-and-transparency`

Potentially three different layers: public evidence, meaning a compact record showing that a protected decision occurred; protected local evidence, meaning the full Candidate Act and receipt retained in protected storage; and authorized later disclosure, meaning a mechanism for proving that the full act matches the earlier public commitment.

This allows the system to separate public transparency from unnecessary real-time disclosure of sensitive operational detail.

The important cryptographic requirement is that later disclosure must match the earlier commitment and must not allow the historical record to be rewritten.

---

### 8. Does spatial finality require GNSS + VIO + odometry in every vehicle?

`context-and-sensors`

No. The architecture should not mandate a fixed sensor stack.

A rule such as "q-of-n independent or sufficiently diverse agreeing sources" is a profile choice, not a universal requirement that every deployment use GNSS, VIO, odometry, radar, LiDAR, or any particular technology.

A vision-centric platform may instead use multiple independently evaluated sources or confidence channels within its own architecture, provided the deployment can justify the relevant independence and uncertainty model.

The core requirement is that the protected boundary must have a defined, auditable basis for deciding whether the context required by the act is sufficiently trustworthy.

The repository should not be read as prescribing a particular commercial sensor strategy.

---

### 9. What if one localization source becomes unavailable or degraded?

`context-and-sensors`

The profile should specify degradation behavior. Possible responses include reducing the permitted motion envelope, increasing the uncertainty margin, requiring a shorter revalidation interval, prohibiting outward motion near a protected boundary, switching to a lower-authority mode, using a Safe-State action, or denying the act if the minimum evidence threshold is no longer met.

A missing sensor must not automatically be treated as a zero-error sensor.

UNKNOWN and EMPTY are intentionally distinct states.

---

### 10. Could strict multi-source agreement become a denial-of-service vector?

`context-and-sensors`

Yes, if implemented naively.

An attacker may attempt to degrade one sensor, create disagreement, or force the system into repeated revalidation.

That is why the policy must separate safety-critical disagreement, expected sensor degradation, source independence, source health, uncertainty expansion, and safe degraded operation.

The finality layer should not attempt to solve sensor fusion by itself. It consumes a protected context decision and applies explicit fail-safe policy to the consequence-bearing act.

---

### 11. How much memory does deterministic encoding and BPC verification require on a small MCU?

`constrained-implementation`

The repository does not claim one fixed footprint. A constrained implementation does not need to instantiate a large general-purpose object model.

Possible implementation strategies include fixed-layout structs, compact integer keys, streaming parsers, preallocated buffers, profile-specific field sets, fixed-size digests, precomputed authority tables, and hardware HMAC/SHA acceleration.

The IETF-facing canonical representation defines interoperability semantics. A production embedded implementation may use a fixed internal representation as long as the externally committed bytes are canonical and unambiguous.

The correct engineering question is not "can a full desktop CBOR stack run at the actuator?" but "what is the smallest deterministic representation and verification path that preserves the required binding semantics on the target hardware?"

---

### 12. Must every Finality Sink parse CBOR?

`constrained-implementation`

No. A Finality Sink may consume a compact, pre-parsed, sink-local capability emitted by the protected enforcement domain: Candidate Act or BPC or richer object -> PED verification -> fixed-size sink capability -> Finality Sink.

The sink can therefore remain extremely small. The full canonical object need not be decoded independently by every actuator microcontroller.

---

### 13. Can the BPC fit inside an 8-byte CAN frame?

`constrained-implementation`

Not in every profile, and that should not be claimed universally.

Possible deployment approaches include a profile-specific reduced BPC, authenticated fragmentation, CAN FD, transport-layer segmentation, a short local Authority Reference plus protected local state, a sink-local capability instead of the original BPC, or a higher-layer gateway that verifies the larger object and emits a compact actuator token.

Classic CAN constraints are therefore an implementation or profile question, not a reason to weaken the binding semantics.

---

### 14. Why not simply use CAN authentication or a MAC on the command?

`comparison-with-existing-mechanisms`

A MAC answers one question: was this message created by an entity holding the key?

Execution finality asks additional questions: is this the exact act that was authorized; is it intended for this sink; is the authority still current; has the nonce already been consumed; has policy or revocation state changed; is the act still inside the authorized envelope; is this controller still the current controller; and can an alternate path bypass the intended sink?

Message authentication is necessary in many deployments, but it is not equivalent to final effectuation authorization.

---

### 15. What happens when a high-rate trajectory envelope is revoked?

`authority-lifecycle-and-revocation`

A production profile should define an immediate transition rule: current envelope valid -> high-rate execution permitted -> revocation or epoch change -> no new permission-expanding setpoints -> enter minimal-risk or Safe-State behavior.

The exact transition may depend on current speed, road geometry, airspace, obstacle state, braking distance, and controller architecture.

The important property is that revocation does not require continuing to honor stale permission merely to preserve liveness.

---

### 16. Does a revocation instantly remove every control output?

`authority-lifecycle-and-revocation`

It should not remove outputs that are independently authorized as necessary safety actions.

For example, a vehicle whose forward-motion envelope is revoked may still need authority to brake.

This is why the architecture distinguishes ordinary consequence-expanding authority, envelope authority, and pre-authorized safety-increasing actions.

Fail-closed at the authority layer should not mean "disable the laws of control."

---

### 17. How is TOCTOU handled between an early authorization check and effectuation?

`authority-lifecycle-and-revocation`

The deciding protected state is re-read close to the final commit. A representative ordering is: static verification, then read current protected state, then consume freshness or nonce, then commit receipt and state update, then release the bounded capability, then effectuation.

An early successful check therefore does not guarantee later effectuation if a relevant generation changes before the protected commit.

This is one of the main differences between "fresh observation" and "commit-time guarantee."

---

### 18. What if revocation changes one microsecond after the atomic commit?

`authority-lifecycle-and-revocation`

No architecture can make a decision depend on information that does not yet exist.

The relevant property is a well-defined linearization point. A deployment must define when authority is considered consumed, when revocation becomes effective, whether a released capability has a bounded lifetime, whether the sink must recheck an epoch, and how much residual exposure is acceptable.

For high-risk actions, the capability can be extremely short-lived and sink-local.

---

### 19. What prevents replay of a valid execution handle?

`authority-lifecycle-and-revocation`

Single-use handles are bound to protected replay state. The reference model expects: nonce unused -> atomic consume -> receipt commit -> capability release.

Concurrent attempts against the same nonce must not result in multiple successful releases.

The repository includes adversarial concurrency testing for this property.

---

### 20. Why is the sink binding necessary if the act is already signed?

`binding-and-path-completeness`

Because the same logical act may have different consequences at different sinks.

A valid authorization for a camera-enable sink must not automatically be reusable at a payload-release sink or a motion-admission sink.

The sink is therefore a load-bearing part of the authority basis.

---

### 21. What if an attacker finds an alternate path around the Finality Sink?

`binding-and-path-completeness`

Then the security claim for that consequence path fails. This is not hidden by the architecture. Path completeness is a protected assumption.

A production deployment must analyze alternate buses, DMA, debug paths, maintenance interfaces, firmware update paths, redundant controllers, power-gating paths, emergency override paths, and direct actuator interfaces.

Execution finality only controls effects that actually traverse the protected boundary.

---

### 22. Does the repository prove hardware non-bypassability?

`binding-and-path-completeness`

No. The repository is a software reference model and red-team harness.

It can demonstrate binding logic, state-machine ordering, replay behavior, generation checks, fragment handling, evidence-key behavior, authority-handover logic, and modeled fault behavior.

It cannot prove physical path completeness on an aircraft or vehicle it has never been integrated into.

---

### 23. Does a valid AER prove that the physical act occurred?

`broadcast-act-evidence`

No. A valid Act Evidence Record proves only what the evidence construction is designed to prove, for example that the protected enforcement domain authenticated a particular decision record under the modeled key and timing assumptions.

It does not by itself prove that a motor moved, that a payload physically released, that a camera actually captured an image, that a vehicle changed trajectory, or that a downstream actuator did not subsequently fail.

Evidence of a protected decision and evidence of physical occurrence are separate problems.

---

### 24. Why use delayed disclosure for AER/KDR instead of signing every act?

`broadcast-act-evidence`

The design goal is compact observer-verifiable evidence on constrained broadcast links.

Delayed disclosure can reduce the per-record public-key overhead while preserving a temporal property: the observer can later verify that the record existed before the relevant secret was disclosed.

The trade-offs include delayed verification, clock assumptions, disclosure scheduling, packet loss, key-chain management, and late-record rejection rules.

It is therefore an optional evidence profile, not a universal replacement for digital signatures.

---

### 25. Can the public chain anchor be used to forge interval 0?

`broadcast-act-evidence`

It must not be. The corrected construction separates K_seed, the never-disclosed protected master seed; K_N, the terminal chain value derived from K_seed; K_i = F(K_(i+1)); K_0 as a public commitment only; and K'_i = F'(K_(i+1)) as the interval tag key.

The public K_0 is not itself an AER authentication secret and must not be transformed into the first interval tag key.

The repository includes negative testing for this specific indexing error.

---

### 26. What if one or more KDR disclosures are lost?

`broadcast-act-evidence`

A later disclosed chain value can recover earlier required chain values by repeated application of the one-way function. This is one reason for the reverse-chain structure.

Packet loss therefore need not make all earlier AERs unverifiable, although the exact retention and recovery window is profile-dependent.

---

### 27. How much clock synchronization does delayed disclosure require?

`broadcast-act-evidence`

The observer must have a bounded timing uncertainty model.

A receiver should reject or discard an AER when its arrival time is too late to establish that the record was received before the corresponding disclosure became usable by an attacker.

The exact Delta, disclosure delay d, and allowed clock uncertainty are deployment parameters.

The architecture should not pretend that delayed-disclosure evidence is secure without a defensible time model.

---

### 28. What happens if the protected receipt store fails?

`protected-state-and-failure`

For a profile that requires durable receipt commitment before release, the rule is: no durable receipt, no ordinary capability release.

This prevents "effectuate first, discover later that the audit or consume state never committed."

A separate Safe-State path may remain available if configured.

---

### 29. Could receipt persistence itself become a denial-of-service target?

`protected-state-and-failure`

Yes. That is a real trade-off.

Mitigations may include redundant protected storage, bounded in-memory protected journals, hardware monotonic counters, failover storage, preallocated log segments, degradation to a smaller Safe-State Set, and explicit availability profiles.

The architecture does not claim that persistence is free. It makes the failure semantics explicit.

---

### 30. Why distinguish UNKNOWN from EMPTY?

`protected-state-and-failure`

Because missing state and confirmed absence are different security conditions.

EMPTY means the protected lookup completed and found no entries. UNKNOWN means the lookup could not establish the state.

Treating UNKNOWN as EMPTY can create authority from missing evidence.

For load-bearing authorization state, the conservative rule is generally: UNKNOWN implies no permission-expanding effectuation.

---

### 31. How does the design handle DAA traffic that changes after a maneuver was computed?

`detect-and-avoid`

The maneuver authority can be bound to a canonical conflict set and Resolution Epoch.

If a new higher-risk intruder appears, an existing track materially changes, uncertainty grows beyond the permitted bound, or the Resolution Epoch is superseded, the old maneuver authorization is no longer applicable at the motion-admission boundary.

The planner may recompute immediately, but computation alone does not preserve the old authority.

---

### 32. Could DAA revalidation cause oscillation or repeated denial?

`detect-and-avoid`

Yes, if the environment changes rapidly or the policy is poorly tuned.

Execution finality does not solve trajectory planning stability. A deployment may need hysteresis, bounded hold intervals, local collision-avoidance priority, emergency safe maneuvers, uncertainty-aware envelopes, and profile-specific revalidation thresholds.

The finality layer ensures that stale basis does not silently remain authority.

---

### 33. How is q-of-n emergency-scene corroboration protected against correlated sensors?

`emergency-scene-profile`

The count should not blindly treat every message as independent evidence.

The profile should account for common physical source, common upstream processor, same credential lineage, same sensor modality, same communication dependency, and known correlation domains.

Two channels carrying the same underlying observation should not automatically count as two independent confirmations.

The repository includes adversarial testing around correlated evidence.

---

### 34. What if all context sensors are consistently wrong?

`threat-model-and-residual-risk`

Then a purely context-based protected decision can still be wrong. Execution finality is not a magical source of truth.

If every trusted input feeding the protected predicate is coherently compromised, the protected boundary may authorize an act on false context.

This is a residual risk and should be stated explicitly.

The architecture reduces unauthorized effectuation relative to its trusted inputs; it does not prove those inputs are physically correct.

---

### 35. What if the PED itself is compromised?

`threat-model-and-residual-risk`

If the protected keys, monotonic state, or verification logic are compromised, the security assumptions are violated.

Possible production mitigations include secure boot, measured boot, hardware key isolation, attestation, redundancy, an independent safety MCU, rollback resistance, protected update paths, tamper response, and key rotation.

The reference harness does not claim to solve compromise of the root of enforcement itself.

---

### 36. Why not rely only on remote attestation?

`comparison-with-existing-mechanisms`

Attestation answers a different question. Attestation can provide evidence about software identity, measured state, device configuration, or execution environment.

Execution finality asks whether this exact pending act may become effective at this sink under the current authority state.

A correctly attested system can still attempt an unauthorized act. Attestation may therefore be an input to execution finality, not a substitute for it.

---

### 37. Why not rely only on OAuth, signed commands, certificates, or ACLs?

`comparison-with-existing-mechanisms`

These mechanisms can establish important authorization context, but they often authorize a principal, a session, an API, a resource class, or a general operation.

Execution finality narrows the final question to exact act, plus exact sink, plus current authority state, plus freshness, plus current context.

The architecture is intended to complement existing authorization systems rather than replace them.

---

### 38. Does the architecture require a trusted centralized authority online for every act?

`offline-operation-and-availability`

No. Profiles may use cached bounded authority, local protected epochs, short-lived grants, pre-authorized envelopes, offline Safe-State behavior, and delayed synchronization.

The key requirement is that offline operation have an explicit bounded authority model rather than silently treating stale cached authority as indefinitely current.

---

### 39. What is the maximum offline window?

`offline-operation-and-availability`

There is no universal value.

The acceptable residual exposure depends on vehicle speed, stopping distance, airspace or road geometry, update frequency, revocation urgency, mission class, consequence severity, and available Safe-State actions.

The repository exposes such values as deployment parameters rather than claiming a single safe constant.

---

### 40. Does fail-closed create a denial-of-service vulnerability?

`offline-operation-and-availability`

Potentially, yes. Any security boundary that can withhold authority can become a target for availability attacks.

The architecture therefore requires explicit consideration of safe degraded modes, bounded cached authority, local safety autonomy, redundant protected state, transport resilience, replay-safe retry, and the distinction between permission-expanding and safety-reducing actions.

Security and liveness must be engineered together.

---

### 41. Can a malicious planner spam the PED with verification requests?

`robustness-and-attack-surface`

Yes. A production implementation may need rate limiting, admission control, priority classes, per-controller quotas, bounded queues, constant-space parsing, authenticated early rejection, and separate safety-critical and non-critical paths.

The repository focuses on authorization semantics, not full resource-exhaustion resistance.

---

### 42. What prevents a large Candidate Act from becoming a parser attack surface?

`robustness-and-attack-surface`

A constrained profile should define maximum object size, maximum nesting, permitted fields, canonical types, integer ranges, fixed-length digests, deterministic ordering, and rejection of unknown or duplicate critical fields.

A safety-critical implementation should not use an unrestricted general-purpose parser at the actuation boundary.

---

### 43. Is deterministic CBOR mandatory?

`encoding-canonicalization-truncation`

The important requirement is deterministic, unambiguous canonicalization for whatever representation is normatively selected.

If the IETF profile uses deterministic CBOR, interoperability tests should verify the exact byte representation.

An implementation may use a different internal structure as long as the protected digest is calculated over the required canonical external representation.

---

### 44. What happens when two semantically equivalent encodings produce different bytes?

`encoding-canonicalization-truncation`

That is precisely why a canonical representation is required. The authority basis must not depend on parser-specific formatting choices.

If two values are intended to be semantically identical under the profile, they must canonicalize to the same committed representation. If the profile does not define that equivalence, they should be treated as different acts.

---

### 45. What if a compact truncated binding collides?

`encoding-canonicalization-truncation`

Truncation introduces explicit risk. The architecture therefore models P_coll ~= q(q-1) / 2^(t+1) and requires the truncation length to be selected against the expected collision domain and risk budget.

A compact commitment should not be treated as collision-free merely because it is cryptographic.

Where ambiguity is detected, the safe response is to deny or request a longer proof rather than guess.

---

### 46. Why not simply use a full 256-bit digest everywhere?

`encoding-canonicalization-truncation`

Some target transports are severely constrained. The architecture therefore separates full internal protected digests, compact transmitted references, and risk-bounded truncation.

Where bandwidth is not constrained, a longer commitment may be preferable. Compactness is a profile optimization, not a security requirement.

---

### 47. How is control-authority handover protected against split brain?

`control-authority-handover`

The protected state contains the current controller and a monotonic Control Authority Epoch. A command is accepted only when command.controller equals CurrentController and command.epoch equals CurrentEpoch.

The intended invariant is that for each governed sink and time, the number of effective ordinary controllers is at most one.

Crash injection is used to test PREPARE, COMMIT, and ENABLE boundaries.

---

### 48. What happens if the new controller crashes after the old controller is revoked?

`control-authority-handover`

The system may temporarily have zero ordinary controllers, which is safer than having two.

A Safe-State controller or pre-authorized fallback behavior may remain active.

The architecture prefers zero ordinary controllers plus safe fallback over two simultaneously authoritative controllers when atomic handover cannot complete.

---

### 49. Does the repository prove the handover protocol for all distributed-system failures?

`control-authority-handover`

No. The finite crash campaign provides evidence about the modeled state machine and tested schedules.

It is not a formal proof over every network partition, storage failure, Byzantine controller, or hardware reset.

A production protocol may additionally require model checking or formal verification.

---

### 50. Why is "evidence is not authority" emphasized?

`architecture-principles`

Because audit artifacts are attractive bearer objects.

If a receipt, AER, attestation result, or observer record can later be replayed as execution authority, the architecture has collapsed two different security roles.

The intended separation is that evidence proves something about a past protected decision, while authority permits a current protected effect. One must not silently substitute for the other.

---

### 51. Can the architecture support existing autopilots and drive-by-wire systems without replacing them?

`deployment-and-scope`

That is the intended deployment model.

The architecture is designed to sit around the consequence boundary, not to replace stabilization, perception, path planning, navigation, braking control, steering control, certified flight-control loops, or existing failsafes.

Existing controllers continue to compute. The finality layer determines whether a proposed consequence may become effective under current protected authority.

---

### 52. Does the architecture require a new hardware chip?

`deployment-and-scope`

No single hardware form is mandated. Possible realizations include a safety MCU, a secure MCU, a TEE, a secure element plus enforcement firmware, an FPGA gate, a protected hypervisor partition, an isolated controller, a network or actuator gateway, or a combination of these.

What matters is whether the deployment actually enforces the required trust and path-completeness properties.

---

### 53. Is this an IETF protocol, a hardware architecture, or both?

`deployment-and-scope`

The work spans both protocol and enforcement concerns, but the IETF-facing material should remain clear about what is being standardized.

Potentially standardizable pieces include compact evidence formats, BPC structure, canonical binding inputs, Authority References, evidence and key-disclosure records, interoperability semantics, failure signaling, and verification rules.

Hardware placement examples are architectural deployment guidance unless a specific interface is standardized.

---

### 54. Why is this relevant to RATS?

`standards-relevance`

Remote attestation can provide trusted evidence about the state of a workload, device, or protected component.

Execution finality can consume that evidence when deciding whether a specific act may become effective: attestation evidence -> protected authority decision -> act-bound execution finality.

The repository does not assume that RATS alone provides actuation authorization.

---

### 55. Why is this relevant to COSE / CBOR?

`standards-relevance`

Constrained deployments need compact canonical representations, authenticated structures, deterministic serialization, key identifiers, algorithm agility, and interoperable test vectors.

Those are natural points of contact with CBOR and COSE engineering.

The execution-finality architecture itself, however, is broader than any one encoding or signature/MAC format.

---

### 56. What is the strongest claim this repository can responsibly make?

`claims-and-falsifiability`

A narrow one: the repository provides an executable reference model and adversarial test harness showing how selected execution-finality invariants can be represented, attacked, and tested under explicit assumptions.

It does not establish airworthiness, automotive functional-safety certification, hardware non-bypassability, universal cryptographic security, production readiness, regulatory compliance, real-world sensor correctness, or complete correctness under every distributed-system failure.

---

### 57. What would falsify the architecture rather than merely expose an implementation bug?

`claims-and-falsifiability`

Examples include a reproducible demonstration that, under the stated assumptions, a materially different act can pass the same protected binding; a valid proof can be moved to another sink without detection; the same single-use nonce can produce two effective releases; stale revocation state can survive the final protected commit; a receipt can fail to commit while ordinary capability is still released; a public delayed-disclosure value enables pre-disclosure forgery; a stale controller epoch can still become effective; two ordinary controllers can become simultaneously effective under the modeled handover protocol; or an explicitly modeled consequence path bypasses the protected sink.

Such counterexamples are exactly what the repository is intended to invite.

---

### 58. What type of external review is most useful?

`review-and-resources`

Useful review includes counterexamples to invariants, alternate-path bypass analysis, low-power MCU timing measurements, CAN and CAN-FD mapping experiments, CBOR canonicalization edge cases, packet-loss traces, delayed-disclosure timing attacks, crash-consistency tests, model checking, formal proofs, DAA stale-state scenarios, Safe-State failure analysis, correlated-sensor attacks, and independent implementations using the same test vectors.

Corrections, negative results, adversarial cases, and implementation criticism are welcome.

---

### 59. Where are the public technical materials?

`review-and-resources`

GitHub reference implementation and red-team harness: https://github.com/sangmdas/UAS-Autonomous-Vehicle-Execution-Finality

IETF Internet-Draft: https://datatracker.ietf.org/doc/draft-das-drip-uas-act-finality/

Broader architectural background: https://zenodo.org/records/22082995 ("The Internet Solved Communication. It Never Solved Authority.")

---

### 60. What is the core principle in one sentence?

`architecture-principles`

Computation, authentication, or possession of a token does not by itself create authority to make a consequential act effective.

---

### 61. What is a Candidate Act?

`terminology`

A Candidate Act is a concrete, fully specified proposed consequence that has been computed, requested, or authenticated but has not yet been made physically effective.

The term exists to make an otherwise invisible distinction explicit. In most systems today there is no separate state between 'the software decided to do this' and 'this is happening'; the write to the actuator register is both.

The architecture inserts that state deliberately. A Candidate Act carries the exact act parameters, the intended sink, and the context on which it depends, and it remains without physical effect until the protected boundary admits it.

---

### 62. What is the Protected Enforcement Domain (PED)?

`terminology`

The PED is the isolated component that verifies a Candidate Act against current protected authority state and controls the physical enablement condition at the sink.

It is defined by properties, not by a product: key isolation, protected monotonic state, verification logic that the general-purpose stack cannot modify at runtime, and placement on every command-to-enablement path for the acts it governs.

It may be realized as a safety MCU, secure MCU, TEE, secure element plus enforcement firmware, FPGA gate, hypervisor partition, isolated controller, or actuator gateway. See also the question on whether new hardware is required.

---

### 63. What is an Execution Handle, and why is it not a bearer token?

`terminology`

An Execution Handle is the object that permits one specific act to become effective at one specific sink, under stated freshness and context conditions.

It is deliberately not a bearer token. Possession is not sufficient: the PED reconstructs the concrete pending act and verifies the handle against that reconstruction, against the sink identity, against current protected state, and against replay state, before consuming it.

This is what allows a compromised component to hold a syntactically valid object and still be unable to cause an effect.

---

### 64. What is a Finality Sink and a withheld enablement condition?

`terminology`

A Finality Sink is the last point at which a decision can still be prevented from becoming physical: an ESC arming line, a latch solenoid driver, a camera power rail, a power-amplifier enable, a mode register, or a motion-admission gate.

The withheld enablement condition is the concrete physical thing the actuator lacks until the PED releases it.

This is the difference between a system where the actuator is always capable and software chooses restraint, and a system where capability itself is conditional. Under compromise, the first offers nothing.

---

### 65. What is the difference between a BPC and an AER? They both look like compact proofs.

`terminology`

They occupy opposite roles and are intentionally non-interchangeable.

A Beacon Proof Capsule (BPC) is verification INPUT: a compact act-bound and sink-bound representation carried to the enforcement boundary over a constrained link, which the PED evaluates. Receiving one is never a reason to act.

An Act Evidence Record (AER) is decision OUTPUT: evidence that the PED made a decision. It is emitted after the fact and must never be accepted as a handle.

Collapsing the two would recreate exactly the bearer-object failure described in the question on why 'evidence is not authority' is emphasized.

---

### 66. Which act classes does the UAS profile define, and why those?

`uas-profile`

The profile defines ARM, KINETIC_ENVELOPE, VOLUME_ENTRY, PAYLOAD_RELEASE, SENSOR_ACTIVATE, RF_EMIT, MODE_TRANSITION, RID_CHANGE, COORDINATED, and a pre-authorized SAFE_STATE class.

They were selected because each maps to a distinct physical sink with a distinct withheld condition, and because together they cover the consequence types a civil UAS can produce: motion, payload, sensing, emission, mode, identity broadcast, and coordinated multi-aircraft action.

Most existing geofencing and mode logic is movement-centric only. Payload, sensor, and RF acts are consequential and are usually ungoverned at the actuator.

---

### 67. Why is RID_CHANGE treated as hostile to the operator?

`uas-profile`

Because the enforcement domain is precisely the component that must not be coercible into making the aircraft anonymous.

A request that would suppress legally required Remote ID transmission is denied unless an authority object explicitly permits the change.

An enforcement boundary that can be told to stop identifying the aircraft is not an enforcement boundary; it is a feature with an off switch.

---

### 68. What does an Observer actually gain, beyond what DRIP authentication already provides today?

`drip-and-remote-id`

DRIP lets an Observer verify, without Internet access, that Broadcast RID messages come from the registered holder of a DRIP Entity Tag. That is identity and message provenance.

The compact act-evidence profile adds a different statement: that a protected enforcement domain, endorsed for that identity, recorded an allow, deny, or safe-state decision for an act class and sink class, before the corresponding key could have been disclosed.

The gain is conduct evidence rather than identity evidence. The limits are stated separately: it does not prove the physical effect occurred, and it does not disclose the act parameters.

---

### 69. Why not simply sign act evidence with the DET key?

`drip-and-remote-id`

Because of where that key lives. On typical airframes the DET or Host Identity key is held by the RID module or the flight software, which is the component whose compromise the mechanism exists to survive.

Evidence signed with that key demonstrates that the aircraft's software emitted it, not that the enforcement domain decided it. A compromised mission computer holding the RID key could broadcast favourable evidence for acts the PED denied.

The default profile therefore uses a distinct evidence key sealed in the PED, endorsed once by the Host Identity key for a validity window. Size, rate, and loss behaviour are additional reasons, but origin is the decisive one.

---

### 70. Does this require a new ASTM F3411 or ICAO carriage code point?

`drip-and-remote-id`

The current draft deliberately does not request a DRIP Frame Type or Specific Authentication Method allocation.

Candidate carriage approaches may require ASTM or ICAO coordination, a future IETF standards effort, or use over Network RID.

The byte-level record construction is separable from the eventual carriage decision, which is why the two questions are kept apart.

---

### 71. Is this a DRIP Working Group work item?

`standards-process`

No. It is an individual Informational Internet-Draft submitted to the IETF standards process for technical discussion. No working-group adoption or code-point allocation is requested in the current version.

Relevance was identified to DRIP, RATS, COSE/CBOR, ACE, SCITT, and T2TRG, and the material is also offered to UAS, Remote ID, constrained-security, automotive, and aviation standards forums.

---

### 72. What is the current status of the draft and the reference implementation?

`standards-process`

The Internet-Draft is published at https://datatracker.ietf.org/doc/draft-das-drip-uas-act-finality/ and the reference implementation and red-team harness at https://github.com/sangmdas/UAS-Autonomous-Vehicle-Execution-Finality.

The draft is Informational and individual. The repository is a reference model and adversarial test harness, not production software.

Both are expected to change in response to review, including negative review.

---

### 73. Does implementing this make an operator compliant with Part 107, U-space, or EASA rules?

`regulatory`

No. This work does not define airworthiness requirements, certification requirements, or legal rules, and it does not decide which acts a regulator permits.

It defines how a permission that has already been issued by the competent authority can be technically enforced at the instant of effect, and how that enforcement can be evidenced to parties who did not issue it.

Compliance remains a matter for the applicable regulator and the applicable certification basis.

---

### 74. How does this relate to certification standards such as DO-178C, DO-254, ISO 26262, ISO 21448, and UL 4600?

`regulatory`

The architecture is complementary to, and dependent on, those processes rather than a substitute for them.

If the enforcement boundary is placed on a safety-relevant path, its software and hardware fall within the applicable assurance process, and the Safe-State Set, degraded modes, and timing behaviour all become items requiring evidence under that process.

A useful framing: functional-safety standards address whether the system behaves correctly under fault; this architecture addresses whether an act is authorized at all under current authority. Neither answers the other's question.

---

### 75. Is there any relationship to the EU AI Act, product liability, or accident investigation?

`regulatory`

Potentially, in the sense that receipts and act evidence produce an auditable record of what was decided and when, which is the kind of artifact that oversight, liability analysis, and investigation regimes tend to require.

The architecture does not claim conformity with any specific instrument, and no regulator has evaluated it. Any such mapping is a matter for the deployment and its legal advisers.

The technically relevant property is narrow: the record must not be rewritable after the fact, and later disclosure must match the earlier commitment.

---

### 76. What are the data-protection implications of broadcasting per-act evidence over a populated area?

`privacy-and-transparency`

They are real and are the reason the privacy-preserving act class exists.

A continuous public stream of fine-grained act parameters would create a behavioural record of operations and, indirectly, of the people and places involved. The profile therefore separates the fact that a protected decision occurred from the disclosure of every parameter of the act.

Deployments should apply data-minimisation to what is broadcast, retain detail in protected local receipts, and disclose that detail through an authorized process rather than over the air.

The repository does not claim that one privacy profile is appropriate for all jurisdictions.

---

### 77. Who issues authority objects, and how is trust bootstrapped?

`keys-and-trust`

Authority originates outside the aircraft or vehicle: corridor approvals, temporary restrictions, geo-zone data, operator credentials, revocations, and payload or sensor permissions come from service suppliers, authority interfaces, fleet operators, and customers.

Enrollment binds the enforcement domain's keys to the platform identity, and the platform identity to the operator's registration, through whatever provisioning process the deployment and its regulator accept.

The architecture assumes this exists and defines what the boundary does with the result. It does not specify a universal enrollment or PKI model, and a weak enrollment process undermines everything downstream.

---

### 78. How are evidence keys rotated, and what happens when a key chain is exhausted?

`keys-and-trust`

Evidence chains are epoch-scoped. A new epoch begins with a fresh protected seed, a fresh chain, a fresh anchor, and a fresh endorsement validity window; the profile requires a new anchor and chain before interval-index reuse rather than attempting to infer a wrapped index.

Ordinary key rotation for enforcement keys is a deployment matter and should follow the platform's key-management and attestation practice.

An implementation that permits index wrap requires an unambiguous lifting rule and is outside the profile.

---

### 79. What if GNSS time or position is spoofed?

`threat-model-and-residual-risk`

Both matter, and in different ways.

Spoofed position is the coherent-context case: if every trusted input feeding the protected predicate agrees and is wrong, the boundary may authorize on false context. This is a stated residual risk, mitigated by source diversity and independence analysis rather than eliminated.

Spoofed time attacks the evidence profile: delayed disclosure depends on a defensible time model, so an observer requires a bounded timing-uncertainty model and must reject records whose arrival time cannot establish pre-disclosure receipt.

A deployment that treats an unauthenticated time source as trusted has weakened both properties.

---

### 80. Does a manual remote-pilot or RC override path bypass the boundary?

`binding-and-path-completeness`

If it reaches the actuator without traversing the protected sink, then yes, and the security claim for that path fails. This is the alternate-path problem stated in concrete form.

Deployments generally must decide explicitly whether manual override is inside or outside the governed set, and document that decision. Safety-increasing actions are normally pre-authorized rather than blocked; permission-expanding manual commands are not privileged merely because a human issued them.

'A human asked for it' is an origin claim. It is subject to the same distinction between origin and contextual permission as any signed command.

---

### 81. How are maintenance, bench-test, and firmware-update modes handled?

`binding-and-path-completeness`

They are among the most common real bypass paths and must be analyzed as such: maintenance interfaces, debug ports, bench harnesses, and update mechanisms can all reach actuators.

A deployment should define whether such modes are physically distinguishable from operational mode, whether they require separate protected authority, whether they are available only with the platform immobilized or on a test rig, and how the protected update path for the enforcement domain itself is authorized.

An enforcement boundary whose own firmware can be replaced through an unprotected path provides no lasting property.

---

### 82. Could this become a remote kill switch, or a tool for grounding fleets?

`threat-model-and-residual-risk`

The concern is legitimate and should be designed against rather than dismissed.

Three properties of the architecture are relevant. Safety-increasing actions are pre-authorized and are not withheld for lack of fresh authority. Offline operation is bounded rather than instantly revoked. And the boundary is designed to resist being coerced into suppressing required identity broadcast.

What remains is a governance question: whoever can issue or revoke authority has real power over the platform, and deployments should define who those parties are, what they may revoke, under what process, and what record is produced. This is properly a matter of regulatory and contractual design, not only cryptography.

---

### 83. What stops an operator from configuring the enforcement domain to allow everything?

`threat-model-and-residual-risk`

At the technical level, nothing prevents a party with full physical and provisioning control over a device from deploying a permissive configuration. The architecture cannot make an operator honest.

What it can do is make the configuration attestable, make decisions evidenced, and make the difference visible to parties who did not issue the authority: an enforcement domain that authorizes everything still produces records, and those records are checkable against the authority that was supposedly in force.

Enforcement against a hostile operator ultimately relies on registration, attestation, audit, and law, with this layer supplying the evidence those processes need.

---

### 84. Why not use a blockchain or distributed ledger for receipts and authority?

`comparison-with-existing-mechanisms`

The load-bearing requirement is at the actuator, in bounded time, often offline, on a constrained device. Consensus latency, availability assumptions, and connectivity requirements are a poor match for deciding whether a solenoid may energize in the next control period.

Receipts additionally need to be produced locally and durably before release, not after global agreement.

Append-only transparency services are relevant later in the pipeline, for audit and non-repudiation of receipts, which is why SCITT is named as a point of contact. That is a different position in the flow from effectuation authority.

---

### 85. How do Finality Receipts relate to later audit, insurance claims, and investigation?

`evidence-and-audit`

A receipt is the protected local record of what was decided, with what basis, at what monotonic position, before release. The compact broadcast record carries only a header and counter, so the two are matched by counter during later analysis.

This gives investigators and insurers something they do not have today: a per-act record produced by a component separate from the autonomy stack that is usually the subject of the investigation.

Retention, chain of custody, protected storage, and access process are deployment matters. Evidence of a protected decision is still not evidence of physical occurrence.

---

### 86. What is the energy and bandwidth overhead on a battery-powered platform?

`constrained-implementation`

The evidence path was designed for this constraint: the per-record onboard operation is a single HMAC-SHA-256 rather than a public-key signature, records are fixed-size, and one key-disclosure record per interval is shared by every record in that interval.

The verification path cost depends on the factors listed under latency, and the repository does not claim a universal figure for either energy or time.

A deployment should measure both on target hardware, including the cost of protected receipt persistence, which is often the dominant term rather than the cryptography.

---

### 87. What is the retrofit story? Can this be added to an existing airframe or vehicle?

`deployment-and-scope`

It depends entirely on whether the enablement condition can be placed on the real consequence path in that platform.

Where an actuator enable line, power rail, or gate is physically accessible and the platform's architecture permits a gateway or safety controller in that position, retrofit is conceivable. Where actuation is deeply integrated and no such placement exists, the property cannot be retrofitted honestly, and claiming it would be worse than not having it.

This is a platform-engineering question, not a protocol question, and it should be answered per platform with an explicit path-completeness analysis.

---

### 88. How does this work in multi-tenant fleets, where manufacturer, operator, and customer all have some authority?

`deployment-and-scope`

The architecture assumes multiple authorities rather than a single one, which is part of why it is relevant to constrained multi-authority work in the IETF.

A deployment must define which party may authorize which act classes, how conflicting authority is resolved, and which party's revocation is effective for which sink. Control-authority handover with monotonic epochs addresses the specific case of two controllers contending for the same governed sink.

Unstated authority relationships are a common source of real-world failure, and the boundary makes them explicit rather than resolving them automatically.

---

### 89. Does any of this apply to weapons, targeting, or counter-UAS?

`deployment-and-scope`

No. Weapons, weapon release, targeting, and counter-UAS engagement are explicitly out of scope for this work, which addresses civil UAS and civil autonomous ground vehicles.

Contributions, profiles, or deployment guidance for those applications are not sought here.

---

### 90. Are there test vectors, and how would two independent implementations be checked against each other?

`review-and-resources`

Interoperability for this kind of mechanism rests on exact bytes: canonical encoding of the binding inputs, the derivation and domain-separation strings, the record layouts, and the verification rules.

Independent implementations exercising the same vectors, including negative vectors for the indexing and truncation errors the harness tests for, are among the most useful contributions available.

Discrepancies found this way should be reported as issues against the repository or raised in the relevant standards discussion.

---

### 91. How should a security issue or a counterexample be reported?

`review-and-resources`

Through the repository's issue tracker for implementation defects and reproducible counterexamples, and by direct contact for anything that should not be public before it is understood.

Counterexamples to the stated invariants are the single most valuable form of contribution, and the falsification list exists to make that target explicit rather than to defend the architecture from it.

---

### 92. Is the architecture patented? What is the licensing posture?

`licensing-and-ipr`

Patent pending. The execution-finality architecture described here is the subject of pending patent applications filed by the author, an independent inventor self-funding the portfolio.

The specification text and this FAQ are published openly for review; the reference implementation is published under the repository's stated licence. Patent rights are expressly reserved and are not licensed by publication alone.

Should any part of the architecture be adopted into an IETF standard, the author's declared position is licensing on fair, reasonable, and non-discriminatory terms, consistent with BCP 79 disclosure obligations. The purpose of publishing specification, mathematics, record formats, and runnable code is adoption and scrutiny, not enclosure.

---

### 93. Does this architecture apply beyond drones and road vehicles?

`architecture-principles`

The invariant is not aviation-specific: an authenticated or correctly computed instruction remains a candidate until the boundary that will make it physical independently verifies the state on which it depends.

That question recurs wherever software can cause irreversible physical or external effect under multiple authorities: industrial actuation, energy systems, medical devices, maritime and rail systems, robotics, and agentic software systems acting through tools.

This repository and draft address civil UAS and civil autonomous ground vehicles. Other domains would need their own act classes, sinks, safe states, and profiles, and their own domain expertise.

---

## Industry Relevance

Where this boundary applies, what the consequential acts are in that setting, and what the
sink and value look like. Named sectors are illustrative; no organization in any sector has
evaluated, endorsed, or adopted this work.

### Parcel delivery and last-mile logistics (UAS)

**Why it matters.** Delivery flights are authorized once, then execute dozens of consequential acts per sortie in populated areas, including the one act that is irreversible in the most literal sense: letting go of the parcel.

**Representative acts.** PAYLOAD_RELEASE, VOLUME_ENTRY, KINETIC_ENVELOPE, SENSOR_ACTIVATE

**Typical sinks.** latch solenoid or winch driver, envelope expansion at the enforcement boundary, motor output register bank

**Value.** A drop can be made conditional on the drop zone, the current restriction state, and position agreement at the moment of release, rather than on the correctness of the mission computer that planned it.

### Infrastructure and asset inspection (UAS)

**Why it matters.** Inspection operates close to boundaries, near critical assets, and usually with sensors running continuously over third-party property.

**Representative acts.** SENSOR_ACTIVATE, KINETIC_ENVELOPE, RF_EMIT

**Typical sinks.** camera power rail or sensor-output key, thrust limit, power-amplifier enable

**Value.** Boundary-proximity revalidation tightens or reduces the permitted envelope as the aircraft approaches a limit, and sensor activation becomes an authorized act rather than a software setting.

### Agriculture and spraying (UAS and ground robots)

**Why it matters.** Dispersal is externally consequential, legally constrained by parcel and buffer boundaries, and irreversible once released.

**Representative acts.** PAYLOAD_RELEASE, KINETIC_ENVELOPE, VOLUME_ENTRY

**Typical sinks.** pump or valve enable, motion-admission gate

**Value.** Buffer-zone compliance becomes a withheld enablement condition rather than a planning assumption, with a per-act record available to the operator and the regulator.

### Survey, mapping, and media production (UAS)

**Why it matters.** The consequential act is often sensing rather than motion, over privacy-sensitive ground, and it is currently ungoverned at the actuator by movement-centric geofencing.

**Representative acts.** SENSOR_ACTIVATE, RF_EMIT, MODE_TRANSITION

**Typical sinks.** camera power rail, frequency register and PA enable

**Value.** Capture over a restricted area can be prevented at the rail, and privacy-preserving evidence lets an observer confirm a protected decision occurred without exposing every operational parameter.

### Public safety, emergency response, and disaster support

**Why it matters.** Temporary restrictions appear during a flight, responder authority is granted ad hoc at a scene, and both must expire reliably.

**Representative acts.** VOLUME_ENTRY, SAFE_STATE, COORDINATED, emergency-scene temporary authority

**Typical sinks.** envelope expansion, motion-admission gate

**Value.** Temporary authority is bound to incident, scene, vehicle, bounded exception, concrete motion, expiry, and independent corroboration, and extinguishes automatically when the scene authority ceases to apply.

### BVLOS operations and urban air mobility support functions

**Why it matters.** Beyond visual line of sight removes the human who would otherwise notice; mode transition into autonomous BVLOS is itself a consequential act.

**Representative acts.** MODE_TRANSITION, KINETIC_ENVELOPE, COORDINATED

**Typical sinks.** flight-mode register, motor output register bank

**Value.** Link loss becomes a stated, auditable exposure bound instead of an open-ended question about cached authority.

### Detect-and-avoid and airspace deconfliction

**Why it matters.** An avoidance maneuver computed against a conflict picture that has since changed is a well-formed instruction, not a valid resolution.

**Representative acts.** DAA resolution finality, KINETIC_ENVELOPE

**Typical sinks.** motion-admission boundary

**Value.** Resolution authority is bound to the conflict set, ownship state, sink, and a monotonic Resolution Epoch, and is revalidated before the maneuver is admitted.

### Autonomous road vehicles and robotaxi fleets

**Why it matters.** Perception, planning, and remote assistance can all emit correctly authenticated instructions that are wrong for the present context, and a fleet is a shared failure domain.

**Representative acts.** motion admission, control-authority handover, emergency-scene temporary authority

**Typical sinks.** protected motion-admission gate

**Value.** The boundary coexists with existing perception, planning, braking, steering, and minimal-risk-control functions, and prevents two otherwise-valid controllers from being simultaneously effective over the same sink.

### Teleoperation and remote assistance

**Why it matters.** Handover between an autonomy stack, a remote operator, and a fallback controller is exactly where split-brain authority appears.

**Representative acts.** control-authority handover, MODE_TRANSITION

**Typical sinks.** motion-admission gate, mode register

**Value.** Monotonic Control Authority Epochs make zero-controller-plus-safe-fallback the failure mode instead of two simultaneously authoritative controllers.

### Ports, mining, construction, and other off-highway autonomy

**Why it matters.** Heavy machinery operating near people, under multiple site authorities, with acts that are irreversible on a human timescale.

**Representative acts.** motion admission, implement or load release, zone entry

**Typical sinks.** hydraulic enable, drive enable, motion-admission gate

**Value.** Site permits and exclusion zones become withheld enablement conditions verified at the machine rather than policies enforced by whichever controller happens to be running.

### Warehouse and intralogistics robotics

**Why it matters.** Dense multi-robot environments with shared floor space, frequent authority changes, and mixed human presence.

**Representative acts.** motion admission, COORDINATED, control-authority handover

**Typical sinks.** drive enable, motion-admission gate

**Value.** Composite semantics in which the prepare step moves nothing and HOLD is a physically safe state, rather than an abstract protocol state.

### Silicon, secure elements, and safety controllers

**Why it matters.** The enforcement boundary must be realized in hardware that isolates keys, holds protected monotonic state, and controls a physical enable line.

**Representative acts.** all classes

**Typical sinks.** gate, rail, or enable line under isolated control

**Value.** A defined set of properties that a safety MCU, secure element, TEE, FPGA gate, or actuator gateway would need to provide, independent of any one vendor architecture.

### Regulators, service suppliers, insurers, and investigators

**Why it matters.** These parties did not issue the authority and cannot rely on operator telemetry alone.

**Representative acts.** evidence and receipt consumption

**Typical sinks.** not applicable

**Value.** Portable, verifiable per-act evidence in defined formats, produced by a component distinct from the autonomy stack that is usually the subject of the inquiry.

---

## Use Cases

| ID | Situation | Gap today | With execution finality |
| --- | --- | --- | --- |
| **UC-01** | **Restriction activated mid-flight** — A delivery aircraft is authorized for a corridor at 14:00. At 14:07 a temporary restriction is activated over part of that corridor for an emergency response. The authorization token held by the ground software remains cryptographically valid. | Whether the aircraft enters depends on whether new geo-zone data reached, and was obeyed by, software that may be stale or compromised. | Entry into the next corridor segment is a distinct act. The boundary reads current generation state inside the atomic consume, so the stale-but-valid token does not release the expanded envelope. |
| **UC-02** | **Compromised mission computer** — The perception or planning stack is fed adversarial input, runs a faulty update, or is controlled by an attacker with root access. | Effective write access to motor registers, ESC arming, the latch driver, or the camera rail turns a software failure into a physical event, and a software geofence on the same processor fails with it. | The compromised component cannot synthesize actuator authority because it never physically held the enablement condition. |
| **UC-03** | **Validly signed but contextually unauthorized command** — A ground station or fleet service sends a correctly authenticated command to release a payload at an unapproved coordinate or disable identity broadcast. | Link authentication establishes that the command came from a key holder, not that the act is permitted in the present context. | The act is verified against current authority, sink, and context before release; identity-suppressing requests are denied unless explicitly permitted. |
| **UC-04** | **Link loss and unbounded cached authority** — The platform loses contact with its operator, service supplier, and revocation source; a revocation is issued after link loss. | Cached authority may continue permitting acts indefinitely, with no stated exposure. | Offline authority is bounded by an explicit window, giving computable time and distance exposure, after which only pre-authorized safe states remain. |
| **UC-05** | **Partially executed coordinated maneuver** — Several aircraft must change formation or hand off an inspection segment together, and the coordination log becomes unreachable mid-sequence. | Some commit and some do not, violating separation assumptions; retries are themselves new physical acts. | Silence never commits, prepare moves no aircraft, HOLD is a physically safe holding maneuver, and compensation is a new act with new authority rather than an undo. |
| **UC-06** | **Observer verification on the ground** — A police officer or facility operator watches a drone lower a payload and activate a camera over a car park. | Identity can be verified cryptographically; conduct cannot be verified at all before the fact, and logs are available only afterwards. | Compact act evidence lets the observer verify, after a short disclosure delay, that the enforcement domain recorded a decision for that act class and sink class before the key could have been disclosed. |
| **UC-07** | **Stale avoidance maneuver** — An avoidance resolution is computed, and before it is executed a new higher-risk intruder appears or an existing track changes materially. | The maneuver executes on the basis it was computed from, because computation and effectuation are the same step. | Authority is bound to the conflict set and Resolution Epoch; the motion-admission boundary revalidates before admitting the maneuver. |
| **UC-08** | **Responder instruction at an incident scene** — A first responder directs an autonomous vehicle to perform a bounded exception to ordinary traffic rules at an incident scene. | Either the vehicle cannot accept the instruction at all, or accepting it depends on general remote-assistance authority with no automatic expiry. | Temporary authority is bound to incident, scene, vehicle, bounded exception, concrete motion, expiry, and independent corroboration, and extinguishes when the scene authority ceases to apply. |
| **UC-09** | **Control handover between autonomy, remote operator, and fallback** — Control of a vehicle or aircraft moves between the onboard stack, a remote operator, and a fallback controller, and one participant crashes mid-handover. | Two controllers can be simultaneously effective, or authority can be ambiguous during the transition. | Protected current-controller state and monotonic epochs bound the effective ordinary controllers to at most one per governed sink, preferring zero plus safe fallback over two. |
| **UC-10** | **Post-incident investigation** — An incident occurs and the investigating party must establish what was authorized, when, and on what basis. | Evidence comes largely from logs produced by the same stack whose behaviour is in question. | Protected receipts are produced by the enforcement domain before release and can be matched by counter to broadcast headers observed at the time. |

---

## Invitation to Review

Most useful contributions:

- Counterexamples to the stated invariants
- Alternate-path bypass analysis on real platforms
- Low-power MCU timing and WCET measurements
- CAN and CAN-FD mapping experiments
- Canonicalization edge cases and negative test vectors
- Delayed-disclosure timing attacks and packet-loss traces
- Crash-consistency testing, model checking, and formal proofs
- Independent implementations exercising the same test vectors

Corrections, negative results, adversarial cases, and implementation criticism are welcome, including on aviation, automotive, and cryptographic assumptions.

---

## Licensing and Patent Status

- **Text of this FAQ and the specification material:** CC BY 4.0
- **Reference implementation:** See repository LICENSE
- **Patent status:** Patent pending; patent rights expressly reserved and not licensed by publication alone
- **Standards posture:** Declared position is FRAND licensing consistent with BCP 79 should any part be adopted into an IETF standard

---

*93 questions across 29 categories (60 in version 1.0, 33 added in 1.1); 13 industry sectors; 10 use cases. Generated from `faq.json`.*
