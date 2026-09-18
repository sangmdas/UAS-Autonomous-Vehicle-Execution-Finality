# System and Test Variables

The repository separates **security variables**, **physical/safety variables**, **network variables**, and **measurement-environment variables** so results can be reproduced instead of being embedded as unexplained constants.

## Cryptographic / compactness variables

| Variable | Meaning | Example |
|---|---|---:|
| `binding_bits` / `t` | retained Binding Commitment bits | 96 |
| `authority_ref_bits` / `r` | compact Authority Reference bits | 64 |
| `bpc_tag_bits` / `m` | BPC authenticator bits | 96 |
| `aer_tag_bits` | AER tag bits | 64 |
| `q` | commitments in collision domain | 100,000 |
| `W` | offline substitution trials | 1,000,000,000 |
| `A_online` | online attempt budget | 1,000 |
| `epsilon_c` | collision probability target | 1e-9 |
| `epsilon_s` | substitution target | 1e-9 |
| `epsilon_f` | forgery target | 1e-9 |

## Spatial variables

| Variable | Meaning |
|---|---|
| `d(t)` | distance to nearest permitted boundary |
| `epsilon_pos` | position uncertainty bound |
| `v_max` | permitted maximum speed |
| `tau` | enforcement-to-actuator reaction latency |
| `a_brk` | guaranteed deceleration used by the model |
| `Delta_r` | maximum revalidation interval |
| `k` | uncertainty multiplier for source consistency |
| `q_min` | minimum agreeing position sources |

## AER variables

`K_seed` is never disclosed. `K_N` is derived from it and is a chain value. `K_0` is public. Evidence interval `i` uses `K'_i = F'(K_(i+1))`, and `K_(i+1)` is disclosed only after the configured delay.

## Environment variables to record for every benchmark

- CPU model and architecture
- logical CPU count
- OS and kernel/platform version
- Python version
- repository commit SHA
- hash/MAC implementation
- persistence backend
- whether measurements include network, secure element, HSM/TEE, filesystem sync, and actuator I/O
- run count, warm-up count, random seed

A result without these fields should be treated as an anecdotal measurement rather than a reproducible benchmark.
