# Candidate Act and Effectuation Boundary

A Candidate Act is represented before it becomes externally effective. The reference harness binds load-bearing fields to a named sink, authority reference, policy/revocation generations, context, freshness, and expiry.

The implementation rule is:

```text
proposed/computed act
        |
        v
  Candidate Act (non-effective)
        |
        v
reconstruct actual pending act at sink
        |
        v
verify current protected state + consume freshness + commit receipt
        |
        v
release bounded local capability
        |
        v
external/physical effect
```

The harness intentionally treats upstream authentication and transport validity as necessary but not sufficient for effectuation.
