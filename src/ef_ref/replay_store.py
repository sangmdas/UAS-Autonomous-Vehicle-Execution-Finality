from __future__ import annotations

import threading


class ReplayStore:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._consumed: set[str] = set()

    def is_consumed(self, nonce: str) -> bool:
        with self._lock:
            return nonce in self._consumed

    def consume_once(self, nonce: str) -> bool:
        with self._lock:
            if nonce in self._consumed:
                return False
            self._consumed.add(nonce)
            return True

    def snapshot(self) -> set[str]:
        with self._lock:
            return set(self._consumed)
