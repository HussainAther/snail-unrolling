# tests/test_eca_restoration.py
import numpy as np

from src.modeling.eca_restoration import (
    _rule_to_lut,
    simulate_eca,
    entropy_series,
    apply_local_perturbation,
    analyze_rule,
)


def test_rule_to_lut_shape():
    lut = _rule_to_lut(30)
    assert lut.shape == (8,)
    assert set(lut.tolist()).issubset({0, 1})


def test_simulate_eca_shape():
    states = simulate_eca(rule=22, n=64, steps=10, seed=0)
    assert states.shape == (11, 64)
    assert states.dtype == np.uint8


def test_entropy_series_length():
    states = simulate_eca(rule=30, n=64, steps=20, seed=1)
    H = entropy_series(states)
    assert len(H) == 21
    assert np.all(np.isfinite(H))


def test_apply_local_perturbation_changes_state():
    s = np.zeros(32, dtype=np.uint8)
    s2 = apply_local_perturbation(s, center=16, width=5, mode="flip")
    assert np.sum(s2) > 0


def test_analyze_rule_coeff_in_range():
    res = analyze_rule(rule=22, n=64, steps=80, seed=0, perturb_at=20, warmup=5, recovery_window=30)
    assert 0.0 <= res.restoration_coefficient <= 1.0

