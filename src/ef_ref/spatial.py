from __future__ import annotations

import math


def stopping_distance(v_max_mps: float, reaction_latency_s: float, guaranteed_deceleration_mps2: float) -> float:
    if guaranteed_deceleration_mps2 <= 0:
        raise ValueError("guaranteed deceleration must be positive")
    return v_max_mps * reaction_latency_s + (v_max_mps ** 2) / (2.0 * guaranteed_deceleration_mps2)


def revalidation_interval(distance_to_boundary_m: float, position_uncertainty_m: float, v_max_mps: float, reaction_latency_s: float, guaranteed_deceleration_mps2: float) -> float:
    if v_max_mps <= 0:
        return math.inf
    s_stop = stopping_distance(v_max_mps, reaction_latency_s, guaranteed_deceleration_mps2)
    return (distance_to_boundary_m - position_uncertainty_m - s_stop) / v_max_mps


def position_consistent(points: list[tuple[float, float]], sigmas: list[float], *, k: float, q_min: int) -> bool:
    if len(points) != len(sigmas):
        raise ValueError("points/sigmas length mismatch")
    if q_min < 1:
        raise ValueError("q_min must be >= 1")
    n = len(points)
    agreeing: set[int] = set()
    for i in range(n):
        for j in range(i + 1, n):
            d = math.dist(points[i], points[j])
            if d <= k * (sigmas[i] + sigmas[j]):
                agreeing.add(i)
                agreeing.add(j)
    return len(agreeing) >= q_min
