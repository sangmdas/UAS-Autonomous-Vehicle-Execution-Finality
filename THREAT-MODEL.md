# Red-Team Threat Model

## Adversary capabilities exercised

The harness assumes an attacker may control or influence the untrusted planner/mission computer, copy valid messages, alter load-bearing act parameters after authorization, redirect an act to another sink, replay a valid proof, race a policy or revocation update, omit or mix fragments, inject stale evidence, exploit public AER anchor material, cause process crashes during controller handover, and submit correlated evidence as if it were independent.

The red-team suite therefore attacks the **binding and state-transition properties**, not just cryptographic primitives.

## Protected assumptions

The model assumes the protected root keys and sink-local keys are not directly disclosed; the hash/HMAC primitives behave as modeled; the protected atomic section is not bypassed; and a physical effect cannot occur through an unmodeled alternate hardware path. The last assumption is deliberately separated because path-completeness is an integration property that cannot be proven by this Python harness alone.

## Explicit non-claims

This repository does **not** demonstrate airworthiness, road-vehicle functional-safety compliance, secure-element resistance, real RF performance, deterministic real-time scheduling, certified braking distance, production cryptographic key management, or absence of alternate physical bypass paths. Those require platform-specific hardware and safety engineering.
