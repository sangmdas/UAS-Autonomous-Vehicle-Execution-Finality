from __future__ import annotations

import math

from .crypto import domain_hash, domain_hmac, trunc_bits, ct_equal
from .models import Fragment


def fragment_payload(payload: bytes, *, session_id: str, key: bytes, mtu: int = 16, tag_bits: int = 64) -> list[Fragment]:
    if mtu <= 0:
        raise ValueError("mtu must be positive")
    total = math.ceil(len(payload) / mtu) or 1
    root = domain_hash("UAS-BPC-FRAG-ROOT", payload)
    out: list[Fragment] = []
    for i in range(total):
        part = payload[i * mtu : (i + 1) * mtu]
        auth = trunc_bits(domain_hmac(key, "UAS-BPC-FRAG", session_id.encode(), root, str(i).encode(), str(total).encode(), part), tag_bits)
        out.append(Fragment(session_id, root, i, total, part, auth))
    return out


def reassemble(fragments: list[Fragment], *, key: bytes) -> bytes | None:
    if not fragments:
        return None
    f0 = fragments[0]
    if len({f.index for f in fragments}) != f0.total:
        return None
    if set(f.index for f in fragments) != set(range(f0.total)):
        return None
    for f in fragments:
        if f.session_id != f0.session_id or f.root != f0.root or f.total != f0.total:
            return None
        expected = trunc_bits(domain_hmac(key, "UAS-BPC-FRAG", f.session_id.encode(), f.root, str(f.index).encode(), str(f.total).encode(), f.payload), len(f.auth) * 8)
        if not ct_equal(expected, f.auth):
            return None
    payload = b"".join(f.payload for f in sorted(fragments, key=lambda x: x.index))
    if domain_hash("UAS-BPC-FRAG-ROOT", payload) != f0.root:
        return None
    return payload
