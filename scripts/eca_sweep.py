# scripts/eca_sweep.py
from __future__ import annotations

import argparse
import json
import os
from typing import List

import numpy as np
import matplotlib.pyplot as plt

from src.modeling.eca_restoration import analyze_rules


def parse_rules(rules_str: str) -> List[int]:
    """
    Accept:
      "22,30,54"
      "0-255"
      "22,30,54,110,126,150"
    """
    rules_str = rules_str.strip()
    if "-" in rules_str and "," not in rules_str:
        a, b = rules_str.split("-", 1)
        return list(range(int(a), int(b) + 1))
    return [int(x.strip()) for x in rules_str.split(",") if x.strip()]


def main():
    p = argparse.ArgumentParser(description="Sweep ECA rules and compute restoration coefficient.")
    p.add_argument("--rules", type=str, default="22,30,54,110,126,150", help="Comma list or range like 0-255")
    p.add_argument("--n", type=int, default=256)
    p.add_argument("--steps", type=int, default=500)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--perturb-at", type=int, default=200)
    p.add_argument("--perturb-width", type=int, default=9)
    p.add_argument("--perturb-mode", type=str, default="flip", choices=["flip", "zero", "one"])
    p.add_argument("--warmup", type=int, default=50)
    p.add_argument("--recovery-window", type=int, default=250)
    p.add_argument("--init", type=str, default="random", choices=["random", "single"])
    p.add_argument("--init-density", type=float, default=0.5)
    p.add_argument("--outdir", type=str, default="outputs")
    p.add_argument("--no-plot", action="store_true")
    args = p.parse_args()

    rules = parse_rules(args.rules)
    os.makedirs(args.outdir, exist_ok=True)

    results = analyze_rules(
        rules,
        n=args.n,
        steps=args.steps,
        seed=args.seed,
        perturb_at=args.perturb_at,
        perturb_width=args.perturb_width,
        perturb_mode=args.perturb_mode,
        warmup=args.warmup,
        recovery_window=args.recovery_window,
        init=args.init,
        init_density=args.init_density,
    )

    out_json = os.path.join(args.outdir, "eca_restoration_results.json")
    payload = [
        {
            "rule": r.rule,
            "restoration_coefficient": r.restoration_coefficient,
            "baseline_mean_entropy": r.baseline_mean_entropy,
            "perturbed_mean_entropy": r.perturbed_mean_entropy,
            "recovery_curve": r.recovery_curve,
        }
        for r in results
    ]
    with open(out_json, "w") as f:
        json.dump(payload, f, indent=2)
    print(f"✅ Wrote {out_json}")

    if args.no_plot:
        return

    # Plot taxonomy scatter
    xs = [r.rule for r in results]
    ys = [r.restoration_coefficient for r in results]

    plt.figure()
    plt.scatter(xs, ys)
    plt.xlabel("ECA rule")
    plt.ylabel("Restoration coefficient")
    plt.title("Restoration coefficient vs ECA rule")
    fig_path = os.path.join(args.outdir, "eca_restoration_taxonomy.png")
    plt.savefig(fig_path, dpi=200, bbox_inches="tight")
    print(f"✅ Wrote {fig_path}")

    # Also plot recovery curves for a few rules
    plt.figure()
    for r in results[: min(6, len(results))]:
        plt.plot(np.array(r.recovery_curve), label=f"rule {r.rule}")
    plt.xlabel("t")
    plt.ylabel("|H_pert(t) - mean(H_base)|")
    plt.title("Recovery curves (subset)")
    plt.legend()
    curve_path = os.path.join(args.outdir, "eca_recovery_curves.png")
    plt.savefig(curve_path, dpi=200, bbox_inches="tight")
    print(f"✅ Wrote {curve_path}")


if __name__ == "__main__":
    main()

