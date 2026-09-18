# Corrected AER/KDR Delayed-Disclosure Construction

The reference implementation deliberately separates the never-disclosed master seed from discloseable chain values.

```text
K_seed <- protected random secret; never disclosed
K_N    = Trunc_128(SHA-256("UAS-AFE-seed" || K_seed || EpochID))
K_i    = F(K_(i+1))
K'_i   = F'(K_(i+1))
```

For evidence interval `i`, the AER authentication key is `K'_i`, while `K_(i+1)` is disclosed only after the configured delay. `K_0` is the public chain commitment and is not an AER authentication secret.

Loss recovery:

```text
K_(i+1) = F^(j-i)(K_(j+1)), j > i
```

A valid tag that arrives after the disclosure safety boundary is discarded because the corresponding secret may already have become public.
