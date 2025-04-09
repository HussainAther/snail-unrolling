# pattern_analysis.py

import cv2
import numpy as np
import matplotlib.pyplot as plt
from src.modeling.turing import run_gray_scott
from src.modeling.cellular_automata import run_1d_ca
from src.analysis.injury_analysis import compare_shell_segments

def generate_turing_pair(save_before, save_after, perturb=True):
    """
    Generate a pair of Turing images (with optional noise/perturbation on 'after').
    """
    U, V = run_gray_scott(width=256, height=256, steps=5000)
    before = (V * 255).astype(np.uint8)
    after = before.copy()

    if perturb:
        noise = np.random.normal(0, 15, before.shape).astype(np.uint8)
        after = cv2.add(after, noise)

    cv2.imwrite(save_before, before)
    cv2.imwrite(save_after, after)
    print(f"Saved simulated unrolled shell patterns:\n- {save_before}\n- {save_after}")

def compare_patterns_with_injury():
    """
    Run full pipeline: simulate patterns and compare before/after injury.
    """
    # Step 1: Generate sample Turing "before" and "after" images
    before_path = "data/processed/unrolled_snail_before.png"
    after_path = "data/processed/unrolled_snail_after.png"
    generate_turing_pair(before_path, after_path, perturb=True)

    # Step 2: Plot and compare real vs synthetic patterns
    ca = run_1d_ca(rule_number=110, width=400, steps=200)

    fig, axs = plt.subplots(1, 3, figsize=(15, 5))
    axs[0].imshow(cv2.imread(before_path, cv2.IMREAD_GRAYSCALE), cmap="inferno")
    axs[0].set_title("Simulated Shell (Before)")
    axs[1].imshow(cv2.imread(after_path, cv2.IMREAD_GRAYSCALE), cmap="inferno")
    axs[1].set_title("Simulated Shell (After)")
    axs[2].imshow(ca, cmap="binary")
    axs[2].set_title("CA Pattern (Rule 110)")
    for ax in axs:
        ax.axis("off")
    plt.tight_layout()
    plt.show()

    # Step 3: Compare difference using SSIM
    score, _ = compare_shell_segments(before_path, after_path, show=True)
    print(f"🩹 Pattern Similarity (SSIM): {score:.4f}")

if __name__ == "__main__":
    compare_patterns_with_injury()

