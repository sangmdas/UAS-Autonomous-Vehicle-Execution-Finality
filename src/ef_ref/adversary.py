from __future__ import annotations

from dataclasses import replace

from .models import CandidateAct, BPC, Fragment, AER


def substitute_param(act: CandidateAct, key: str, value) -> CandidateAct:
    p = dict(act.params)
    p[key] = value
    return replace(act, params=p)


def substitute_sink(act: CandidateAct, sink_id: str) -> CandidateAct:
    return replace(act, sink_id=sink_id)


def stale_policy(act: CandidateAct, epoch: int) -> CandidateAct:
    return replace(act, policy_epoch=epoch)


def corrupt_fragment(fragment: Fragment) -> Fragment:
    if not fragment.payload:
        return replace(fragment, payload=b"X")
    b = bytearray(fragment.payload)
    b[0] ^= 0x01
    return replace(fragment, payload=bytes(b))


def retag_aer_with_public_anchor(aer: AER, anchor_k0: bytes) -> AER:
    """Attacker mistake used in a negative test: public K0 must not be a usable interval tag key."""
    from .crypto import domain_hmac, trunc_bits
    from .aer import EvidenceChain
    leaked_candidate = EvidenceChain.Fprime(anchor_k0)
    tag = trunc_bits(domain_hmac(leaked_candidate, "UAS-AFE-rec", aer.device_id.encode(), aer.epoch_id.encode(), aer.header), len(aer.tag) * 8)
    return replace(aer, tag=tag)
