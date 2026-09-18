from __future__ import annotations

import math

from .crypto import domain_hash, domain_hmac, trunc_bits, ct_equal
from .models import AER, KDR


class EvidenceChain:
    """Corrected delayed-disclosure construction.

    K_seed is never disclosed. K_N is derived from it and is a chain value.
    Evidence interval i uses K'_i = F'(K_(i+1)).
    """

    def __init__(self, *, k_seed: bytes, device_id: str, epoch_id: str, chain_length: int, interval_ms: int = 1000, delay_intervals: int = 3, tag_bits: int = 64) -> None:
        if chain_length < 2:
            raise ValueError("chain_length must be >= 2")
        if delay_intervals < 1:
            raise ValueError("delay_intervals must be >= 1")
        self.k_seed = k_seed
        self.device_id = device_id
        self.epoch_id = epoch_id
        self.N = chain_length
        self.interval_ms = interval_ms
        self.delay = delay_intervals
        self.tag_bits = tag_bits
        self._keys: list[bytes] = [b""] * (self.N + 1)
        self._keys[self.N] = trunc_bits(domain_hash("UAS-AFE-seed", k_seed, epoch_id.encode()), 128)
        for i in range(self.N - 1, -1, -1):
            self._keys[i] = self.F(self._keys[i + 1])

    @staticmethod
    def F(x: bytes) -> bytes:
        return trunc_bits(domain_hash("UAS-AFE-chain", x), 128)

    @staticmethod
    def Fprime(x: bytes) -> bytes:
        return trunc_bits(domain_hash("UAS-AFE-tag", x), 128)

    @property
    def anchor_k0(self) -> bytes:
        return self._keys[0]

    def tag_key(self, interval: int) -> bytes:
        if interval < 0 or interval >= self.N:
            raise IndexError(interval)
        return self.Fprime(self._keys[interval + 1])

    def make_aer(self, *, interval: int, act_class: str, decision: str, sink_class: str, receipt_counter: int) -> AER:
        header = f"{interval}|{act_class}|{decision}|{sink_class}|{receipt_counter}".encode()
        tag = trunc_bits(domain_hmac(self.tag_key(interval), "UAS-AFE-rec", self.device_id.encode(), self.epoch_id.encode(), header), self.tag_bits)
        return AER(self.device_id, self.epoch_id, interval, act_class, decision, sink_class, receipt_counter, header, tag)

    def disclose_for_interval(self, evidence_interval: int) -> KDR:
        if evidence_interval < 0 or evidence_interval >= self.N:
            raise IndexError(evidence_interval)
        return KDR(self.epoch_id, evidence_interval, evidence_interval + 1, self._keys[evidence_interval + 1])


class Observer:
    def __init__(self, *, device_id: str, epoch_id: str, anchor_k0: bytes, delay_intervals: int, interval_ms: int, clock_uncertainty_ms: int = 0) -> None:
        self.device_id = device_id
        self.epoch_id = epoch_id
        self.anchor_k0 = anchor_k0
        self.delay = delay_intervals
        self.interval_ms = interval_ms
        self.clock_uncertainty_ms = clock_uncertainty_ms
        self.last_interval = -1
        self.last_key = anchor_k0
        self.pending: dict[int, list[AER]] = {}

    def receive_aer(self, aer: AER, *, receive_time_ms: int, epoch_start_ms: int = 0) -> bool:
        if aer.device_id != self.device_id or aer.epoch_id != self.epoch_id:
            return False
        x = math.floor((receive_time_ms + self.clock_uncertainty_ms - epoch_start_ms) / self.interval_ms)
        if x >= aer.interval + self.delay:
            return False
        self.pending.setdefault(aer.interval, []).append(aer)
        return True

    def _iterate(self, key: bytes, count: int) -> bytes:
        out = key
        for _ in range(count):
            out = EvidenceChain.F(out)
        return out

    def receive_kdr(self, kdr: KDR) -> list[AER]:
        if kdr.epoch_id != self.epoch_id:
            return []
        j = kdr.evidence_interval
        if j <= self.last_interval:
            return []
        # last_key is K_(last_interval+1), except initial state last_interval=-1 => K_0.
        steps = j - self.last_interval
        if not ct_equal(self._iterate(kdr.key, steps), self.last_key):
            return []
        verified: list[AER] = []
        for i in range(self.last_interval + 1, j + 1):
            k_for_i = self._iterate(kdr.key, j - i)  # K_(i+1)
            tag_key = EvidenceChain.Fprime(k_for_i)
            for aer in self.pending.get(i, []):
                expected = trunc_bits(domain_hmac(tag_key, "UAS-AFE-rec", self.device_id.encode(), self.epoch_id.encode(), aer.header), len(aer.tag) * 8)
                if ct_equal(expected, aer.tag):
                    verified.append(aer)
        self.last_interval = j
        self.last_key = kdr.key
        return verified
