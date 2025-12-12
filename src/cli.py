# src/cli.py
import argparse
from projection.flatten import polar_unroll
import cv2

def main():
    parser = argparse.ArgumentParser(description="Unroll snail shell images.")
    parser.add_argument("input", help="Path to input image")
    parser.add_argument("output", help="Path to save unrolled output")
    args = parser.parse_args()

    image = cv2.imread(args.input)
    if image is None:
        print(f"Error: couldn't read {args.input}")
        return

    unrolled = polar_unroll(image)
    cv2.imwrite(args.output, unrolled)
    print(f"Saved unrolled image to {args.output}")

if __name__ == "__main__":
    main()

