# src/modeling/cellular_automata.py

import numpy as np
import matplotlib.pyplot as plt

def apply_rule(triplet, rule_bin):
    """
    Apply rule to a triplet of cells.
    """
    index = int("".join(str(bit) for bit in triplet), 2)
    return int(rule_bin[7 - index])  # reverse for correct Wolfram ordering

def run_1d_ca(rule_number=30, width=400, steps=200):
    """
    Run a 1D cellular automaton with a given rule number.
    
    Returns:
        ca (ndarray): Binary matrix of automaton evolution
    """
    rule_bin = f"{rule_number:08b}"  # e.g. '00011110' for Rule 30
    ca = np.zeros((steps, width), dtype=np.uint8)
    ca[0, width // 2] = 1  # Initial seed in the center

    for t in range(1, steps):
        for x in range(1, width - 1):
            neighborhood = ca[t-1, x-1:x+2]
            ca[t, x] = apply_rule(neighborhood, rule_bin)

    return ca

def plot_automaton(ca, cmap='binary'):
    """
    Plot the 1D CA result.
    """
    plt.figure(figsize=(10, 6))
    plt.imshow(ca, cmap=cmap, interpolation='nearest')
    plt.axis('off')
    plt.title("1D Cellular Automaton Pattern")
    plt.tight_layout()
    plt.show()

# Example usage
if __name__ == "__main__":
    ca = run_1d_ca(rule_number=110, width=400, steps=200)
    plot_automaton(ca)

