from __future__ import annotations

import threading
from dataclasses import asdict

from .crypto import canonical_bytes, sha256
from .models import Receipt


class ReceiptStoreUnavailable(RuntimeError):
    pass


class ReceiptStore:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._receipts: list[Receipt] = []
        self.available = True

    def last_digest(self) -> bytes:
        with self._lock:
            if not self._receipts:
                return b"\x00" * 32
            return sha256(canonical_bytes(self._serializable(self._receipts[-1])))

    def next_counter(self) -> int:
        with self._lock:
            return len(self._receipts) + 1

    def commit(self, receipt: Receipt) -> None:
        with self._lock:
            if not self.available:
                raise ReceiptStoreUnavailable("receipt store unavailable")
            if receipt.counter != len(self._receipts) + 1:
                raise ValueError("non-monotonic receipt counter")
            expected_prev = b"\x00" * 32 if not self._receipts else sha256(
                canonical_bytes(self._serializable(self._receipts[-1]))
            )
            if receipt.previous_digest != expected_prev:
                raise ValueError("receipt chain mismatch")
            self._receipts.append(receipt)

    @staticmethod
    def _serializable(r: Receipt) -> dict:
        d = asdict(r)
        for k, v in list(d.items()):
            if isinstance(v, bytes):
                d[k] = v.hex()
        return d

    def snapshot(self) -> list[Receipt]:
        with self._lock:
            return list(self._receipts)
