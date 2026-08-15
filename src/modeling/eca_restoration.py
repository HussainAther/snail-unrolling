# src/modeling/eca_restoration.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import numpy as np


@dataclass
class RestorationResult:
    rule: int
    restoration_coefficient: float
    baseline_mean_entropy: float
    perturbed_mean_entropy: float
    recovery_curve: List[float]  # distance-to-baseline over time


def _rule_to_lut(rule: int) -> np.ndarray:
    """
    Convert ECA rule number [0..255] into a lookup table of length 8.
    Neighborhood ordering: 111,110,101,100,011,010,001,000
    """
    if not (0 <= rule <= 255):
        raise ValueError("rule must be in [0, 255]")
    bits = np.array([(rule >> i) & 1 for i in range(8)], dtype=np.uint8)
    return bits[::-1]  # reverse so index 0 corresponds to 111


def step_eca(state: np.ndarray, lut: np.ndarray) -> np.ndarray:
    """
    One ECA step with periodic boundary conditions.
    state: shape (n,), values {0,1}
    lut: shape (8,), mapping neighborhood->new cell
    """
    left = np.roll(state, 1)
    center = state
    right = np.roll(state, -1)
    # neighborhood code in [0..7] where 111 -> 7, 000 -> 0
    code = (left << 2) | (center << 1) | right
    # lut is ordered [111..000], so index = 7-code
    return lut[7 - code]


def shannon_entropy(p: float, eps: float = 1e-12) -> float:
    """
    Binary Shannon entropy of Bernoulli(p), in bits.
    """
    p = float(np.clip(p, eps, 1.0 - eps))
    return -(p * np.log2(p) + (1.0 - p) * np.log2(1.0 - p))


def entropy_series(states: np.ndarray) -> np.ndarray:
    """
    states: shape (t, n)
    Returns entropy over time based on fraction of 1s at each t.
    """
    p = states.mean(axis=1)
    return np.array([shannon_entropy(pi) for pi in p], dtype=float)


def simulate_eca(
    rule: int,
    n: int = 256,
    steps: int = 400,
    seed: Optional[int] = 0,
    init: str = "random",
    init_density: float = 0.5,
) -> np.ndarray:
    """
    Returns states of shape (steps+1, n)
    """
    rng = np.random.default_rng(seed)
    lut = _rule_to_lut(rule)

    if init == "single":
        state = np.zeros((n,), dtype=np.uint8)
        state[n // 2] = 1
    elif init == "random":
        state = (rng.random(n) < init_density).astype(np.uint8)
    else:
        raise ValueError("init must be 'random' or 'single'")

    states = np.zeros((steps + 1, n), dtype=np.uint8)
    states[0] = state
    for t in range(steps):
        state = step_eca(state, lut)
        states[t + 1] = state
    return states


def apply_local_perturbation(
    state: np.ndarray,
    center: Optional[int] = None,
    width: int = 9,
    mode: str = "flip",
) -> np.ndarray:
    """
    Perturb a copy of state locally around `center` with size `width`.
    mode:
      - 'flip': 0->1, 1->0 in region
      - 'zero': set region to 0
      - 'one': set region to 1
    """
    if width <= 0:
        raise ValueError("width must be > 0")

    n = state.shape[0]
    out = state.copy()
    if center is None:
        center = n // 2

    half = width // 2
    idx = (np.arange(center - half, center - half + width) % n).astype(int)

    if mode == "flip":
        out[idx] = 1 - out[idx]
    elif mode == "zero":
        out[idx] = 0
    elif mode == "one":
        out[idx] = 1
    else:
        raise ValueError("mode must be 'flip', 'zero', or 'one'")
    return out


def restoration_coefficient(
    baseline_entropy: np.ndarray,
    perturbed_entropy: np.ndarray,
    warmup: int = 50,
    recovery_window: int = 250,
) -> Tuple[float, List[float], float, float]:
    """
    Compute a simple restoration coefficient based on entropy deviation.

    baseline_entropy, perturbed_entropy: arrays length T
    warmup: ignore early transient for baseline mean
    recovery_window: time region after perturbation to score recovery

    Returns:
      coeff in [0,1], recovery_curve, baseline_mean, perturbed_mean
    """
    if baseline_entropy.shape != perturbed_entropy.shape:
        raise ValueError("entropy series must have same shape")

    T = len(baseline_entropy)
    warmup = int(max(0, warmup))
    recovery_window = int(max(1, recovery_window))

    baseline_mean = float(np.mean(baseline_entropy[warmup:])) if warmup < T else float(np.mean(baseline_entropy))
    perturbed_mean = float(np.mean(perturbed_entropy[warmup:])) if warmup < T else float(np.mean(perturbed_entropy))

    # Distance-to-baseline mean over time (absolute deviation)
    dist = np.abs(perturbed_entropy - baseline_mean)
    curve = dist.tolist()

    # Score: how much deviation remains, averaged over a post-perturbation window.
    # We want *lower* residual deviation => higher restoration.
    start = max(warmup, 0)
    end = min(T, start + recovery_window)
    residual = float(np.mean(dist[start:end]))

    # Normalize using a conservative scale: baseline entropy variability + small epsilon
    scale = float(np.std(baseline_entropy[warmup:]) + 1e-6)
    # If baseline is very stable, scale is tiny; clamp to avoid division blowups
    scale = max(scale, 1e-3)

    # Convert residual to [0,1] where 1 is perfect restoration
    coeff = float(np.exp(-residual / scale))
    coeff = float(np.clip(coeff, 0.0, 1.0))
    return coeff, curve, baseline_mean, perturbed_mean


def analyze_rule(
    rule: int,
    n: int = 256,
    steps: int = 500,
    seed: int = 0,
    perturb_at: int = 200,
    perturb_width: int = 9,
    perturb_mode: str = "flip",
    warmup: int = 50,
    recovery_window: int = 250,
    init: str = "random",
    init_density: float = 0.5,
) -> RestorationResult:
    """
    Run baseline and perturbed simulation for one rule.
    """
    # Baseline
    states_base = simulate_eca(rule, n=n, steps=steps, seed=seed, init=init, init_density=init_density)
    H_base = entropy_series(states_base)

    # Perturbed: identical start, then perturb at time perturb_at
    # Re-simulate so that we can inject a perturbation mid-run.
    rng_seed = seed  # keep deterministic
    lut = _rule_to_lut(rule)

    if init == "single":
        state = np.zeros((n,), dtype=np.uint8)
        state[n // 2] = 1
    else:
        rng = np.random.default_rng(rng_seed)
        state = (rng.random(n) < init_density).astype(np.uint8)

    states_pert = np.zeros((steps + 1, n), dtype=np.uint8)
    states_pert[0] = state
    for t in range(steps):
        if t == perturb_at:
            state = apply_local_perturbation(state, center=n // 2, width=perturb_width, mode=perturb_mode)
        state = step_eca(state, lut)
        states_pert[t + 1] = state

    H_pert = entropy_series(states_pert)

    coeff, curve, base_mean, pert_mean = restoration_coefficient(
        H_base,
        H_pert,
        warmup=warmup,
        recovery_window=recovery_window,
    )

    return RestorationResult(
        rule=rule,
        restoration_coefficient=coeff,
        baseline_mean_entropy=base_mean,
        perturbed_mean_entropy=pert_mean,
        recovery_curve=curve,
    )


def analyze_rules(
    rules: List[int],
    **kwargs,
) -> List[RestorationResult]:
    return [analyze_rule(rule=r, **kwargs) for r in rules]

