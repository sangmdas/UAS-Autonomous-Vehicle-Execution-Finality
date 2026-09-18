import math


def collision_probability(q: int, t: int) -> float:
    return q*(q-1)/(2**(t+1))


def substitution_probability(work: int, t: int) -> float:
    return work/(2**t)


def minimum_bits_for_collision(q: int, epsilon: float) -> int:
    return math.ceil(math.log2(q*(q-1)/(2*epsilon)))


def minimum_bits_for_substitution(work: int, epsilon: float) -> int:
    return math.ceil(math.log2(work/epsilon))


def test_collision_formula_and_inverse_are_consistent():
    q=100_000; eps=1e-9
    t=minimum_bits_for_collision(q, eps)
    assert collision_probability(q,t) <= eps


def test_offline_substitution_formula_and_inverse_are_consistent():
    w=1_000_000_000; eps=1e-9
    t=minimum_bits_for_substitution(w,eps)
    assert substitution_probability(w,t) <= eps


def test_64_bits_not_automatically_safe_for_large_offline_budget():
    assert substitution_probability(1_000_000_000,64) > 1e-12
