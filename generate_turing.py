import argparse
import cv2
import numpy as np
from src.modeling.turing import run_gray_scott, plot_pattern

def main(output_path="turing_pattern.png", steps=5000):
    U, V = run_gray_scott(steps=steps)
    img = (V * 255).astype("uint8")
    cv2.imwrite(output_path, img)
    print(f"Turing pattern saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a Turing reaction-diffusion pattern")
    parser.add_argument("--output", type=str, default="turing_pattern.png", help="Output path for pattern image")
    parser.add_argument("--steps", type=int, default=5000, help="Number of simulation steps")
    args = parser.parse_args()

    main(output_path=args.output, steps=args.steps)

