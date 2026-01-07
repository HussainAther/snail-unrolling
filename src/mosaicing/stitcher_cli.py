import argparse
import os
import cv2
from mosaicing.stitcher import stitch_images

def main():
    parser = argparse.ArgumentParser(description="Stitch strips horizontally.")
    parser.add_argument("--folder", type=str, default="data/processed", help="Folder containing strip images")
    parser.add_argument("--output", type=str, default="stitched_output.png", help="Path to save stitched image")

    args = parser.parse_args()

    result = stitch_images(strips_folder=args.folder)
    cv2.imwrite(args.output, result)
    print(f"Saved stitched image to {args.output}")

if __name__ == "__main__":
    main()

