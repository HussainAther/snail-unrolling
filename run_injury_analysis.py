# run_injury_analysis.py

import argparse
import cv2
import numpy as np
import matplotlib.pyplot as plt
from src.modeling.turing import run_gray_scott
from src.analysis.injury_analysis import compare_shell_segments

def generate_turing_pattern_pair(save_before, save_after, perturb=True):
    U, V = run_gray_scott(width=256, height=256, steps=5000)
    before = (V * 255).astype(np.uint8)
    after = before.copy()

    if perturb:
        noise = np.random.normal(0, 15, before.shape).astype(np.uint8)
        after = cv2.add(after, noise)

    cv2.imwrite(save_before, before)
    cv2.imwrite(save_after, after)
    print(f"[✔] Saved simulated shell images:\n- {save_before}\n- {save_after}")

def main():
    parser = argparse.ArgumentParser(
        description="Simulate and compare Turing shell patterns before and after injury."
    )
    parser.add_argument("--save_before", type=str, required=True, help="Path to save the 'before' image")
    parser.add_argument("--save_after", type=str, required=True, help="Path to save the 'after' image")
    parser.add_argument("--perturb", action="store_true", help="Add noise to simulate injury")
    parser.add_argument("--compare", action="store_true", help="Run SSIM comparison after generating")
    args = parser.parse_args()

    generate_turing_pattern_pair(args.save_before, args.save_after, perturb=args.perturb)

    if args.compare:
        score, _ = compare_shell_segments(args.save_before, args.save_after, show=True)
        print(f"🧠 SSIM Pattern Similarity Score: {score:.4f}")

if __name__ == "__main__":
    main()

