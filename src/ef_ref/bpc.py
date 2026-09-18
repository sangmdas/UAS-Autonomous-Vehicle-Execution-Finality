from __future__ import annotations

from dataclasses import asdict

from .crypto import canonical_bytes, domain_hash, domain_hmac, trunc_bits, hkdf_sha256, ct_equal
from .models import CandidateAct, BPC


def act_digest(act: CandidateAct) -> bytes:
    return domain_hash("UAS-BPC-ACT", canonical_bytes(act.to_dict()))


def context_digest(context: dict) -> bytes:
    return domain_hash("UAS-BPC-CTX", canonical_bytes(context))


def derive_session_keys(root: bytes, *, session_nonce: str, device_id: str, policy_epoch: int, sink_id: str) -> tuple[bytes, bytes]:
    k_b = hkdf_sha256(root, f"BEACON|{session_nonce}|{device_id}|{policy_epoch}|{sink_id}".encode())
    k_bind = hkdf_sha256(root, f"BIND|{session_nonce}|{device_id}|{sink_id}".encode())
    return k_b, k_bind


def binding_full(act: CandidateAct, k_bind: bytes) -> bytes:
    da = act_digest(act)
    dc = context_digest(act.context)
    payload = b"|".join([
        da,
        act.sink_id.encode(),
        act.authority_ref.encode(),
        str(act.policy_epoch).encode(),
        str(act.revocation_epoch).encode(),
        dc,
        act.nonce.encode(),
        str(act.expiry_ms).encode(),
    ])
    return domain_hmac(k_bind, "UAS-BPC-BIND", payload)


def generate_bpc(act: CandidateAct, *, root: bytes, session_nonce: str, binding_bits: int = 96, tag_bits: int = 96) -> BPC:
    k_b, k_bind = derive_session_keys(root, session_nonce=session_nonce, device_id=act.device_id, policy_epoch=act.policy_epoch, sink_id=act.sink_id)
    da = act_digest(act)
    dc = context_digest(act.context)
    b = binding_full(act, k_bind)
    b_t = trunc_bits(b, binding_bits)
    unsigned = {
        "device_id": act.device_id,
        "act_class": act.act_class,
        "sink_id": act.sink_id,
        "authority_ref": act.authority_ref,
        "policy_epoch": act.policy_epoch,
        "revocation_epoch": act.revocation_epoch,
        "freshness": act.nonce,
        "expiry_ms": act.expiry_ms,
        "act_digest": da.hex(),
        "context_digest": dc.hex(),
        "binding_trunc": b_t.hex(),
    }
    tag = trunc_bits(domain_hmac(k_b, "UAS-BPC-CAPSULE", canonical_bytes(unsigned)), tag_bits)
    return BPC(tag=tag, **{**unsigned, "act_digest": da, "context_digest": dc, "binding_trunc": b_t})


def verify_bpc_transport(bpc: BPC, *, root: bytes, session_nonce: str, tag_bits: int | None = None) -> bool:
    k_b, _ = derive_session_keys(root, session_nonce=session_nonce, device_id=bpc.device_id, policy_epoch=bpc.policy_epoch, sink_id=bpc.sink_id)
    unsigned = asdict(bpc)
    tag = unsigned.pop("tag")
    for k in ("act_digest", "context_digest", "binding_trunc"):
        unsigned[k] = unsigned[k].hex()
    expected = domain_hmac(k_b, "UAS-BPC-CAPSULE", canonical_bytes(unsigned))
    expected = trunc_bits(expected, len(tag) * 8 if tag_bits is None else tag_bits)
    return ct_equal(tag, expected)
