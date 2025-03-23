# pattern_analysis.py

import cv2
import numpy as np
import matplotlib.pyplot as plt
from src.modeling.turing import run_gray_scott
from src.modeling.cellular_automata import run_1d_ca

def load_real_shell(path):
    """
    Load a real unrolled snail shell image (flattened).
    """
    img = cv2.imread(path)
    if img is None:
        raise FileNotFoundError(f"Could not load image: {path}")
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img_rgb

def compare_patterns(shell_path=None, save_path="pattern_comparison.png"):
    """
    Run Turing and Cellular Automata models and compare with real shell.
    """
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))

    # Load real shell if provided
    if shell_path:
        shell_img = load_real_shell(shell_path)
        axs[0].imshow(shell_img)
        axs[0].set_title("Real Unrolled Shell")
    else:
        axs[0].axis('off')
        axs[0].set_title("No Shell Image")

    # Turing pattern (reaction-diffusion)
    U, V = run_gray_scott(width=256, height=256, steps=5000)
    axs[1].imshow(V, cmap="inferno")
    axs[1].set_title("Turing Pattern")

    # Cellular Automata
    ca = run_1d_ca(rule_number=110, width=400, steps=200)
    axs[2].imshow(ca, cmap="binary", interpolation="nearest")
    axs[2].set_title("Cellular Automaton (Rule 110)")

    for ax in axs:
        ax.axis("off")

    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.show()
    print(f"Pattern comparison saved to {save_path}")

# Example usage
if __name__ == "__main__":
    # Optional: provide real unrolled shell path
    # real_shell = "data/processed/unrolled_snail.png"
    real_shell = None
    compare_patterns(shell_path=real_shell)

