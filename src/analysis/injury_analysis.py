# src/analysis/injury_analysis.py

import cv2
import numpy as np
import matplotlib.pyplot as plt
import json
import os
from skimage.metrics import structural_similarity as ssim

def load_and_prepare(path, size=(512, 512)):
    """
    Load and resize an image for comparison.
    """
    img = cv2.imread(path)
    if img is None:
        raise FileNotFoundError(f"Could not load image: {path}")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, size)
    return img

def compare_shell_segments(before_path, after_path, show=True):
    """
    Compare pre- and post-injury unrolled shell segments.
    """
    before = cv2.imread(before_path, cv2.IMREAD_GRAYSCALE)
    after = cv2.imread(after_path, cv2.IMREAD_GRAYSCALE)

    score, diff = ssim(before, after, full=True)
    diff = (diff * 255).astype("uint8")

    if show:
        fig, axs = plt.subplots(1, 3, figsize=(15, 5))
        axs[0].imshow(before, cmap='gray')
        axs[0].set_title("Before Injury")
        axs[1].imshow(after, cmap='gray')
        axs[1].set_title("After Injury")
        axs[2].imshow(diff, cmap='inferno')
        axs[2].set_title(f"SSIM Difference Map\nScore = {score:.4f}") 
        cv2.imshow("SSIM Map", diff)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        for ax in axs:
            ax.axis('off')
        plt.tight_layout()
        plt.show()

    return score, diff

def save_ssim_result(score, before_path, after_path, output_path="ssim_result.json"):
    result = {
        "before_image": os.path.basename(before_path),
        "after_image": os.path.basename(after_path),
        "ssim_score": float(score)
    }
    with open(output_path, "w") as f:
        json.dump(result, f, indent=4)

# Example usage
if __name__ == "__main__":
    before_img = "data/processed/unrolled_snail_before.png"
    after_img = "data/processed/unrolled_snail_after.png"
    score, _ = compare_shell_segments(before_img, after_img, show=True)

    print(f"SSIM Score: {score:.4f}")

    save_ssim_result(
        score=score,
        before_path=before_img,
        after_path=after_img,
        output_path="ssim_result.json"
    )
    print(f"SSIM Similarity Score: {score:.4f}")

