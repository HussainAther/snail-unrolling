# src/modeling/turing.py

import numpy as np
import matplotlib.pyplot as plt

def run_gray_scott(width=200, height=200, Du=0.16, Dv=0.08, F=0.035, k=0.06, steps=10000):
    """
    Simulate Gray-Scott reaction-diffusion system.
    
    Returns:
        U, V (ndarrays): Concentrations of chemical A (U) and B (V)
    """
    U = np.ones((height, width))
    V = np.zeros((height, width))

    # Seed initial square in center
    r = 20
    U[height//2 - r:height//2 + r, width//2 - r:width//2 + r] = 0.50
    V[height//2 - r:height//2 + r, width//2 - r:width//2 + r] = 0.25

    def laplacian(Z):
        return (
            -4 * Z
            + np.roll(Z, (0, -1), (0, 1))
            + np.roll(Z, (0, 1), (0, 1))
            + np.roll(Z, (-1, 0), (0, 1))
            + np.roll(Z, (1, 0), (0, 1))
        )

    for i in range(steps):
        Lu = laplacian(U)
        Lv = laplacian(V)
        uvv = U * V * V
        U += (Du * Lu - uvv + F * (1 - U))
        V += (Dv * Lv + uvv - (F + k) * V)

        if i % 1000 == 0:
            print(f"Step {i}/{steps}")

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

