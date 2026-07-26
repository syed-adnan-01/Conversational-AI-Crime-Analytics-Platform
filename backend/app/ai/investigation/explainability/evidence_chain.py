"""Evidence chain helpers."""

from __future__ import annotations

from typing import Iterable


def build_evidence_chain(references: Iterable[str]) -> list[str]:
    return [ref for ref in references if ref]
