import numpy as np

from modeling.turing import run_gray_scott


def test_turing_output_shapes():
    """Turing model should return two same-shaped arrays."""
    U, V = run_gray_scott(steps=10)

    assert isinstance(U, np.ndarray)
    assert isinstance(V, np.ndarray)
    assert U.shape == V.shape
    assert U.ndim == 2


def test_turing_value_ranges():
    """Turing concentrations should stay within reasonable bounds."""
    U, V = run_gray_scott(steps=20)

    assert np.all(U >= 0)
    assert np.all(V >= 0)
    assert np.max(U) <= 1.5
    assert np.max(V) <= 1.5

