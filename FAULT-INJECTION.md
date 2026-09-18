# Fault-Injection Plan for a Hardware Port

The Python harness establishes testable state-machine expectations. A hardware implementation should reproduce the same invariants while injecting faults around the actual protected-state and effectuation boundaries.

## Atomic finality commit checkpoints

Instrument at least these checkpoints:

```text
F0 before deciding current-state read
F1 after deciding current-state read
F2 after replay reservation / nonce consume
F3 after receipt payload constructed
F4 after receipt durable commit
F5 after capability generation
F6 after sink accepts capability
F7 after actuator command crosses the effectuation boundary
```

Reset or power-fail at every checkpoint. After recovery, record:

- current policy/revocation epochs;
- replay/nonce state;
- receipt-chain head;
- capability state;
- actuator/sink state;
- current controller and authority epoch;
- safe-state selection.

Required property for single-use acts: no recovery path may produce a second effective release from the same consumed freshness value.

## Persistence backends

Repeat against the actual persistence technologies used by the target: secure element, TPM/HSM, FRAM, flash journal, protected filesystem, database, or replicated state service. Record write atomicity and durability assumptions explicitly.
