from __future__ import annotations

from .models import ControlState


class InjectedCrash(RuntimeError):
    pass


class HandoverController:
    def __init__(self, state: ControlState) -> None:
        self.state = state

    def prepare(self, new_controller: str) -> None:
        if self.state.pending_controller is not None:
            raise ValueError("handover already pending")
        self.state.pending_controller = new_controller
        self.state.pending_epoch = self.state.current_epoch + 1

    def commit(self) -> None:
        if self.state.pending_controller is None or self.state.pending_epoch is None:
            raise ValueError("nothing prepared")
        # Revoke old ordinary authority before the new controller is enabled.
        self.state.safe_only = True
        self.state.current_epoch = self.state.pending_epoch

    def enable(self) -> None:
        if self.state.pending_controller is None or self.state.pending_epoch != self.state.current_epoch:
            raise ValueError("invalid pending handover")
        self.state.current_controller = self.state.pending_controller
        self.state.pending_controller = None
        self.state.pending_epoch = None
        self.state.safe_only = False

    def transactional_handover(self, new_controller: str, crash_at: str | None = None) -> None:
        self.prepare(new_controller)
        if crash_at == "after_prepare":
            raise InjectedCrash(crash_at)
        self.commit()
        if crash_at == "after_commit":
            raise InjectedCrash(crash_at)
        self.enable()
        if crash_at == "after_enable":
            raise InjectedCrash(crash_at)

    def accepts(self, *, controller: str, epoch: int, sink_id: str, act_value: float) -> bool:
        if sink_id != self.state.sink_id or self.state.safe_only:
            return False
        lo = float(self.state.current_envelope.get("min", float("-inf")))
        hi = float(self.state.current_envelope.get("max", float("inf")))
        return controller == self.state.current_controller and epoch == self.state.current_epoch and lo <= act_value <= hi

    def effective_authority_count(self, controllers: list[tuple[str, int]]) -> int:
        return sum(1 for c, e in controllers if self.accepts(controller=c, epoch=e, sink_id=self.state.sink_id, act_value=0.0))
