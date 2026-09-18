# Benchmark Interpretation

The benchmark scripts intentionally measure only the local Python reference harness unless explicitly stated otherwise.

**Do not describe these numbers as flight-controller, ECU, secure-element, network, or certified actuator latency.** They exclude real radio propagation, secure-element/HSM access, durable production databases, RTOS scheduling, hardware buses, motor/ESC dynamics, braking response, and safety-monitor latency.

For each metric report p50, p95, p99, maximum, operation count, environment, and commit SHA when available.

The useful engineering question is not whether Python is fast enough for a vehicle. It is whether the architecture decomposes into measurable operations whose real implementations can be benchmarked independently: parse, lookup, MAC/hash, replay consume, currentness read, receipt commit, comparison, capability release, and evidence-tag generation.
