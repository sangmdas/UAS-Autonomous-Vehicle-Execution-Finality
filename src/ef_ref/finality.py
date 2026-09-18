from __future__ import annotations

import threading
from dataclasses import dataclass

from .bpc import act_digest, binding_full, context_digest, derive_session_keys, verify_bpc_transport
from .crypto import ct_equal, domain_hmac, trunc_bits
from .models import CandidateAct, AuthorityState, BPC, Receipt
from .receipt_store import ReceiptStore, ReceiptStoreUnavailable
from .replay_store import ReplayStore


@dataclass(frozen=True)
class Decision:
    allowed: bool
    reason: str
    capability: bytes | None = None
    receipt_counter: int | None = None


class FinalitySink:
    """Single-process model of protected sink-side atomic verify/consume/commit/release."""

    def __init__(self, *, root_key: bytes, sink_key: bytes, replay_store: ReplayStore | None = None, receipt_store: ReceiptStore | None = None) -> None:
        self.root_key = root_key
        self.sink_key = sink_key
        self.replay = replay_store or ReplayStore()
        self.receipts = receipt_store or ReceiptStore()
        self._atomic = threading.Lock()
        self.policy_epoch = 1
        self.revocation_epoch = 1

    def set_epochs(self, policy: int | None = None, revocation: int | None = None) -> None:
        with self._atomic:
            if policy is not None:
                self.policy_epoch = policy
            if revocation is not None:
                self.revocation_epoch = revocation

    def _capability(self, binding: bytes, act: CandidateAct, counter: int) -> bytes:
        envelope = str(sorted(act.params.items())).encode()
        return trunc_bits(domain_hmac(self.sink_key, "SINK-CAP", binding, act.sink_id.encode(), envelope, str(counter).encode()), 128)

    def verify_and_effectuate(
        self,
        *,
        actual_act: CandidateAct,
        bpc: BPC,
        authority: AuthorityState,
        session_nonce: str,
        now_ms: int,
        pre_commit_hook=None,
    ) -> Decision:
        # Cold/early checks may reject cheaply, but are not final currentness checks.
        if not verify_bpc_transport(bpc, root=self.root_key, session_nonce=session_nonce):
            return Decision(False, "INVALID_BPC_TAG")
        if bpc.device_id != actual_act.device_id:
            return Decision(False, "DEVICE_MISMATCH")
        if bpc.sink_id != actual_act.sink_id:
            return Decision(False, "SINK_MISMATCH")
        if bpc.authority_ref != actual_act.authority_ref:
            return Decision(False, "AUTHORITY_REF_MISMATCH")
        if bpc.act_class != actual_act.act_class:
            return Decision(False, "ACT_CLASS_MISMATCH")
        if now_ms > min(bpc.expiry_ms, authority.expiry_ms, actual_act.expiry_ms):
            return Decision(False, "EXPIRED")
        if actual_act.device_id != authority.device_id or actual_act.act_class not in authority.allowed_classes or actual_act.sink_id not in authority.sink_ids:
            return Decision(False, "AUTHORITY_SCOPE")
        if not ct_equal(bpc.act_digest, act_digest(actual_act)):
            return Decision(False, "ACT_MISMATCH")
        if not ct_equal(bpc.context_digest, context_digest(actual_act.context)):
            return Decision(False, "CONTEXT_MISMATCH")
        _, k_bind = derive_session_keys(self.root_key, session_nonce=session_nonce, device_id=actual_act.device_id, policy_epoch=bpc.policy_epoch, sink_id=actual_act.sink_id)
        binding = binding_full(actual_act, k_bind)
        if not ct_equal(bpc.binding_trunc, binding[: len(bpc.binding_trunc)]):
            return Decision(False, "BINDING_MISMATCH")

        if pre_commit_hook is not None:
            pre_commit_hook()

        # Atomic finality commit: deciding epochs -> replay consume -> receipt commit -> capability release.
        with self._atomic:
            if bpc.policy_epoch != self.policy_epoch or actual_act.policy_epoch != self.policy_epoch or authority.min_policy_epoch > self.policy_epoch:
                return Decision(False, "POLICY_EPOCH_MISMATCH")
            if bpc.revocation_epoch != self.revocation_epoch or actual_act.revocation_epoch != self.revocation_epoch or authority.min_revocation_epoch > self.revocation_epoch:
                return Decision(False, "REVOCATION_EPOCH_MISMATCH")
            if not self.replay.consume_once(actual_act.nonce):
                return Decision(False, "REPLAY")
            counter = self.receipts.next_counter()
            receipt = Receipt(
                counter=counter,
                decision="ALLOW",
                act_digest=act_digest(actual_act),
                binding=binding,
                sink_id=actual_act.sink_id,
                context_digest=context_digest(actual_act.context),
                nonce=actual_act.nonce,
                previous_digest=self.receipts.last_digest(),
            )
            try:
                self.receipts.commit(receipt)
            except ReceiptStoreUnavailable:
                # Fail closed. Nonce remains consumed, preventing ambiguous retry/effect.
                return Decision(False, "RECEIPT_STORE_UNAVAILABLE")
            cap = self._capability(binding, actual_act, counter)
            return Decision(True, "ALLOW", cap, counter)
