import argparse
import cv2
from src.modeling.turing import run_gray_scott


def save_pattern_image(U, output_path="turing_pattern.png"):
    img = (U * 255).astype("uint8")
    cv2.imwrite(output_path, img)
    print(f"Turing pattern saved to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Generate and save a Turing pattern image")
    parser.add_argument("--steps", type=int, default=5000, help="Number of simulation steps")
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility")
    parser.add_argument("--output", type=str, default="turing_pattern.png", help="Output image path")
    args = parser.parse_args()

    U, _ = run_gray_scott(steps=args.steps, seed=args.seed)
    save_pattern_image(U, args.output)


if __name__ == "__main__":
    main()

