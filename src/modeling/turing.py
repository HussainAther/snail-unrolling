# src/modeling/turing.py

import numpy as np
import matplotlib.pyplot as plt

def run_gray_scott(steps=5000):
    # Initialize fields
    size = 256
    U = np.ones((size, size))
    V = np.zeros((size, size))
    r = 20
    U[size//2 - r:size//2 + r, size//2 - r:size//2 + r] = 0.50
    V[size//2 - r:size//2 + r, size//2 - r:size//2 + r] = 0.25

    # Constants
    Du, Dv, F, k = 0.16, 0.08, 0.035, 0.065

    for _ in range(steps):
        Lu = cv2.Laplacian(U, cv2.CV_64F)
        Lv = cv2.Laplacian(V, cv2.CV_64F)
        U += Du * Lu - U * V**2 + F * (1 - U)
        V += Dv * Lv + U * V**2 - (F + k) * V

    return U, V

def plot_pattern(U, V, cmap='inferno'):
    """
    Visualize the chemical concentration as an image.
    """
    pattern = V  # often V shows stronger patterns
    plt.figure(figsize=(6, 6))
    plt.imshow(pattern, cmap=cmap)
    plt.axis('off')
    plt.title("Turing Pattern (Gray-Scott)")
    plt.tight_layout()
    plt.show()

# Example usage
if __name__ == "__main__":
    U, V = run_gray_scott(256, 256, steps=8000)
    plot_pattern(U, V)

