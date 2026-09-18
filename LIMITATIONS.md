# Limitations — What This Repository Does Not Prove

This repository is a **reference implementation, adversarial test harness, and reproducibility package** for the execution-finality mechanisms described in the accompanying technical work. Its purpose is to make architectural invariants executable and falsifiable under explicit assumptions.

Passing the included tests is useful evidence about the **included model and implementation**. It is not a general proof about every deployment, vehicle, aircraft, radio, controller, operating environment, or third-party product.

## 1. It does not prove airworthiness or vehicle safety certification

The repository does not establish compliance with, certification under, or equivalence to any aviation, automotive, robotics, functional-safety, or cybersecurity assurance regime. In particular, it is not an airworthiness approval, type certification, operational authorization, functional-safety case, safety-of-the-intended-functionality case, or production cybersecurity certification.

The DAA, motion-admission, emergency-scene, and control-handover models are reference constructions. They require platform-specific hazard analysis, independent verification, environmental testing, and safety engineering before use in a real consequential system.

## 2. It does not prove hardware non-bypassability

The software harness models a Protected Enforcement Domain and Finality Sink. It does not prove that a real implementation prevents all bypass paths through:

- debug or maintenance interfaces;
- DMA or shared-memory paths;
- alternate buses;
- actuator fallback modes;
- bootloader or firmware-update paths;
- compromised peripheral controllers;
- physical tampering;
- side channels;
- fault injection; or
- undocumented hardware behavior.

The repository includes a fault-injection plan, but the packaged tests are not a substitute for hardware fault injection on the actual target platform.

## 3. It does not prove real-time or worst-case timing

The benchmark results are local reference-harness measurements. They do not establish:

- worst-case execution time;
- deterministic scheduling latency;
- hard real-time deadlines;
- ISR or RTOS behavior;
- bus arbitration delay;
- flash/EEPROM/HSM write latency;
- durable `fsync` or power-loss behavior;
- RF propagation or retransmission delay;
- actuator response time; or
- end-to-end control-loop stability.

The packaged Python measurements explicitly exclude production secure-element/HSM access, real actuator I/O, RF transport, durable storage, and certified control hardware.

## 4. It does not prove cryptographic security in the formal sense

The repository implements representative constructions using standard primitives, but the test suite is not a formal cryptographic proof, certification, or cryptanalytic review.

It does not establish resistance to every possible:

- side-channel attack;
- key-extraction attack;
- implementation flaw;
- entropy failure;
- RNG compromise;
- microarchitectural attack;
- fault attack; or
- future cryptanalytic development.

The security of truncated fields remains dependent on the stated attacker-work, collision, forgery, rate-limit, freshness, and operational assumptions.

## 5. It does not prove that every consequential path is covered

The architecture requires consequence-path completeness: every path capable of making a protected act effective must pass through the relevant enforcement boundary.

The harness tests the modeled paths. It cannot prove that an external implementation has no undocumented or unintended alternate effectuation path. That requires platform-specific architecture review, hardware inspection, integration testing, and adversarial validation.

## 6. It does not prove that an AER means the physical act occurred

A verified Act Evidence Record (AER), under the modeled construction, supports the conclusion that the protected evidence mechanism authenticated a decision record for the stated interval and binding context.

It does **not**, by itself, prove that:

- the physical act actually occurred;
- the act completed successfully;
- the external world changed as expected;
- the policy itself was legally or ethically correct;
- the sensor inputs were truthful; or
- every relevant evidence record was received by an observer.

AER/KDR evidence is deliberately distinct from execution authority and from independent physical-event proof.

## 7. It does not prove DAA safety for real airspace

The included conflict-set and closest-point-of-approach mathematics are illustrative engineering models for testing the execution-finality boundary around an accepted maneuver.

They are not a certified Detect-and-Avoid algorithm, collision-avoidance standard, well-clear definition, surveillance-performance specification, or operational safety case. Real DAA behavior depends on sensor quality, encounter models, aircraft dynamics, latency, airspace rules, contingency handling, and certification requirements outside this harness.

## 8. It does not prove emergency-scene evidence is trustworthy in the field

The emergency-scene q-of-n tests verify the modeled independence and threshold logic. They do not prove that real cameras, V2X messages, responder credentials, maps, roadside units, or other evidence channels are authentic, independent, uncompromised, correctly classified, or free from common-mode failure.

Physical-source independence and anti-spoofing must be established in the deployment architecture.

## 9. It does not prove distributed handover correctness under every network model

The control-authority handover tests exercise the included protected state machine, crash points, stale epochs, and split-brain conditions. The seeded randomized campaign is finite.

It does not constitute a proof of consensus, liveness, partition tolerance, or correctness for every possible distributed-system failure, Byzantine participant, storage fault, or recovery topology.

## 10. Finite tests are not exhaustive proof

The packaged snapshot reports:

- **66 automated tests passed**; and
- **5,000 seeded randomized handover crash schedules with zero modeled dual-authority violations**.

Those results mean that no violation was observed in those executed tests under the stated implementation and assumptions. They do not prove that no defect exists, that all state combinations were explored, or that a different implementation will behave identically.

## 11. It is not a penetration test of third-party products

The red-team suite attacks the included reference implementation and simulator. It does not claim to have tested, reverse engineered, penetrated, or found defects in any named UAV, vehicle, avionics, autonomy, cloud, telecom, semiconductor, or other third-party product.

Named companies or technologies in related documentation are contextual examples only unless a separate source explicitly states otherwise.

## 12. It does not prove regulatory or legal compliance

The repository does not provide legal advice and does not establish compliance with aviation law, traffic law, privacy law, product-safety law, spectrum rules, cybersecurity regulations, data-protection law, or any jurisdiction-specific approval requirement.

A technically enforced policy may still be legally wrong, incomplete, stale, or inapplicable.

## 13. It does not prove patentability, validity, infringement, or standard essentiality

The repository may demonstrate technical implementation and reproducibility, but it does not establish:

- patent novelty;
- inventive step / non-obviousness;
- sufficiency or enablement under any particular patent law;
- validity of any patent or patent application;
- freedom to operate;
- infringement by any third party;
- essentiality to any standard; or
- entitlement to any particular licensing outcome.

Copyright permission under CC BY-NC 4.0 is separate from patent rights. See `IPR-NOTICE.md`.

## 14. It does not prove production readiness

Before a real deployment, at minimum, the following would normally require separate engineering evidence:

- target-hardware porting;
- protected boot and key provisioning;
- secure-element/HSM/TEE integration;
- durable atomic storage behavior;
- brownout and reset testing;
- actuator/bus/path-completeness analysis;
- WCET and real-time scheduling analysis;
- sensor and clock trust analysis;
- RF/interoperability testing;
- key lifecycle and recovery procedures;
- fleet-scale load and long-duration testing;
- safety-case integration;
- independent security review; and
- applicable regulatory/certification testing.

## What a passing run *does* support

Within the stated model and assumptions, a passing run supports a narrower, testable statement:

> The included reference implementation exhibited the specified execution-finality invariants for the executed positive, negative, race, replay, fragmentation, delayed-disclosure, DAA, emergency-scene, and control-handover tests, and no invariant violation was observed in the packaged seeded randomized campaign.

That is intentionally narrower than a claim of real-world safety, certification, security proof, or production fitness.
