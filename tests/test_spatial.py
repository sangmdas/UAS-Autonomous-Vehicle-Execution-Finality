import math

from ef_ref.spatial import stopping_distance, revalidation_interval, position_consistent


def test_worked_example_60m():
    s = stopping_distance(15, 0.1, 5)
    assert math.isclose(s, 24.0)
    dt = revalidation_interval(60, 5, 15, 0.1, 5)
    assert math.isclose(dt, 31/15, rel_tol=1e-12)


def test_worked_example_30m():
    dt = revalidation_interval(30, 5, 15, 0.1, 5)
    assert math.isclose(dt, 1/15, rel_tol=1e-12)


def test_speed_reduction_restores_margin():
    s = stopping_distance(8, 0.1, 5)
    assert math.isclose(s, 7.2)
    dt = revalidation_interval(30, 5, 8, 0.1, 5)
    assert math.isclose(dt, 17.8/8, rel_tol=1e-12)


def test_nonpositive_interval_requires_hold_or_safe_action():
    assert revalidation_interval(10, 5, 15, 0.1, 5) <= 0


def test_two_consistent_sources_pass():
    assert position_consistent([(0,0),(1,1),(100,100)], [1,1,1], k=1.0, q_min=2)


def test_insufficient_consistent_sources_fail():
    assert not position_consistent([(0,0),(20,20),(100,100)], [1,1,1], k=1.0, q_min=2)
