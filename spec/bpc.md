# Beacon Proof Capsule (BPC) Reference Profile

The reference BPC uses deterministic serialization, a domain-separated act digest, context digest, keyed binding, truncation, and a whole-capsule authenticator.

Representative equations:

```text
D_A = SHA-256("UAS-BPC-ACT" || canonical(CandidateAct))
D_C = SHA-256("UAS-BPC-CTX" || canonical(Context))

B = HMAC(K_bind,
         "UAS-BPC-BIND" || D_A || SinkID || AuthorityRef ||
         PolicyEpoch || RevocationEpoch || D_C || Nonce || Expiry)

B_t = Trunc_t(B)
```

The BPC is verification input. It is never interpreted as effectuation authority merely because it authenticated correctly.
