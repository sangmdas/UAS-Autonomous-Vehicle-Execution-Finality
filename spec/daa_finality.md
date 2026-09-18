# Conflict-Set-Bound DAA Finality

The maneuver is bound to the deterministic root of the complete relevant conflict set and to a monotonic Resolution Epoch.

```text
C_root = H(CanonicalSort(Intruder_1 ... Intruder_n))
Accept(M) => M.resolution_epoch == CurrentResolutionEpoch
Accept(M) => M.conflict_root == CurrentConflictRoot
```

The test harness also evaluates an illustrative closest-point-of-approach margin for every relevant intruder. One unsafe or stale relevant track makes the entire maneuver non-admissible in this profile.
