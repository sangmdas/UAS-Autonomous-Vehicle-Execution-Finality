# Atomic Control-Authority Handover

The reference state machine models:

```text
PREPARE B
   -> B pending, A still ordinary controller
COMMIT
   -> old ordinary authority revoked; epoch advanced; SAFE_ONLY gap
ENABLE B
   -> B becomes current controller; SAFE_ONLY ends
```

At all observable points:

```text
sum_c EffectiveAuthority(c, sink, epoch, time) <= 1
```

Crash injection occurs after PREPARE, COMMIT, and ENABLE to test that split-brain authority is never produced.
