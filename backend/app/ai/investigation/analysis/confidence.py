"""Confidence calculation helpers."""

from __future__ import annotations

from typing import Iterable

from app.ai.investigation.intelligence.investigation_models import ConfidenceLevel


def clamp_score(score: float) -> float:
    return max(0.0, min(1.0, score))


def level_from_score(score: float) -> ConfidenceLevel:
    if score >= 0.75:
        return ConfidenceLevel.HIGH
    if score >= 0.45:
        return ConfidenceLevel.MEDIUM
    return ConfidenceLevel.LOW


def blend_confidence(scores: Iterable[float], weights: Iterable[float] | None = None) -> float:
    score_list = [clamp_score(score) for score in scores]
    if not score_list:
        return 0.0
    if weights is None:
        return sum(score_list) / len(score_list)
    weight_list = [max(0.0, float(weight)) for weight in weights]
    if not weight_list or len(weight_list) != len(score_list):
        return sum(score_list) / len(score_list)
    total_weight = sum(weight_list)
    if total_weight <= 0:
        return sum(score_list) / len(score_list)
    return sum(score * weight for score, weight in zip(score_list, weight_list)) / total_weight


def confidence_to_percent(score: float) -> float:
    return round(clamp_score(score) * 100.0, 2)
