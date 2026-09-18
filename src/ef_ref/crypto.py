from __future__ import annotations

import hashlib
import hmac
import json
from typing import Any


def canonical_bytes(obj: Any) -> bytes:
    """Deterministic JSON used only for this reference harness."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def hmac_sha256(key: bytes, data: bytes) -> bytes:
    return hmac.new(key, data, hashlib.sha256).digest()


def trunc_bits(data: bytes, bits: int) -> bytes:
    if bits <= 0 or bits % 8 != 0:
        raise ValueError("reference harness supports positive byte-aligned truncation only")
    n = bits // 8
    if n > len(data):
        raise ValueError("cannot retain more bits than input contains")
    return data[:n]


def hkdf_sha256(ikm: bytes, info: bytes, length: int = 32, salt: bytes | None = None) -> bytes:
    """Minimal RFC5869-style HKDF for deterministic local tests."""
    if salt is None:
        salt = b"\x00" * hashlib.sha256().digest_size
    prk = hmac_sha256(salt, ikm)
    out = b""
    t = b""
    counter = 1
    while len(out) < length:
        t = hmac_sha256(prk, t + info + bytes([counter]))
        out += t
        counter += 1
    return out[:length]


def domain_hash(label: str, *parts: bytes) -> bytes:
    return sha256(label.encode("utf-8") + b"\x00" + b"".join(parts))


def domain_hmac(key: bytes, label: str, *parts: bytes) -> bytes:
    return hmac_sha256(key, label.encode("utf-8") + b"\x00" + b"".join(parts))


def ct_equal(a: bytes, b: bytes) -> bool:
    return hmac.compare_digest(a, b)
