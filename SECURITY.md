# Security Testing Policy

This repository is designed for defensive architecture evaluation. Tests should target the included reference harness, test vectors, or systems for which the tester has authorization.

Preferred reports include:

- exact invariant violated;
- test configuration and random seed;
- minimal reproducer;
- expected vs actual decision;
- whether the failure is cryptographic, state-machine, concurrency, transport, or integration related.

Do not report a benchmark-only performance limitation as a security bypass unless it changes an enforced invariant.
