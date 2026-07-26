"""Operational trace recorder for investigation execution."""

from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter


@dataclass(slots=True)
class TraceEvent:
    name: str
    detail: str
    elapsed_ms: float


class InvestigationTrace:
    """Captures execution timings and a compact audit trail."""

    def __init__(self, case_id: str | None = None):
        self.case_id = case_id
        self.events: list[TraceEvent] = []
        self.timings_ms: dict[str, float] = {}
        self._started: dict[str, float] = {}

    def start(self, name: str) -> None:
        self._started[name] = perf_counter()

    def end(self, name: str, detail: str = "") -> None:
        started = self._started.pop(name, None)
        elapsed_ms = 0.0
        if started is not None:
            elapsed_ms = (perf_counter() - started) * 1000.0
            self.timings_ms[name] = elapsed_ms
        self.events.append(TraceEvent(name=name, detail=detail, elapsed_ms=elapsed_ms))
