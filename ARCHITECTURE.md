# Architecture

## Trust split

```text
+---------------------------+
| Planner / mission / AI    |  computes proposals
+-------------+-------------+
              |
              v
+---------------------------+
| Protected Enforcement     |
| Domain                    |
| - protected keys          |
| - current policy/revoke   |
| - replay state            |
| - receipt state           |
+-------------+-------------+
              |
              | bounded release/capability
              v
+---------------------------+
| Finality Sink             |  first consequence-bearing boundary
+-------------+-------------+
              |
              v
        physical/external effect
```

## Core atomic sequence

```text
ReadCurrentState <= Validate <= ConsumeFreshness <= CommitReceipt < ReleaseCapability < Effectuate
```

The harness represents the final deciding policy/revocation read, freshness consumption, receipt commit, and capability release inside one protected critical section.

## Evidence plane is separate

AER/KDR/Anchor/Receipt objects describe or later prove a decision. They are never accepted by the reference Finality Sink as execution authorization.
