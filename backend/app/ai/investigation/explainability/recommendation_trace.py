"""Recommendation trace helpers."""

from __future__ import annotations

from typing import Iterable


def build_recommendation_trace(reasons: Iterable[str]) -> list[str]:
    return [reason for reason in reasons if reason]
