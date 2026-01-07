import argparse
import os
import cv2
from mosaicing.stitcher import stitch_images, load_strips

def main():
    parser = argparse.ArgumentParser(description="Stitch strips horizontally.")
    parser.add_argument("--folder", type=str, default="data/processed", help="Folder containing strip images")
    parser.add_argument("--output", type=str, default="stitched_output.png", help="Path to save stitched image")
    parser.add_argument("--dry-run", action="store_true", help="Preview only; do not save stitched image")

    args = parser.parse_args()

    strips = load_strips(args.folder)

    if args.dry_run:
        total_width = sum(img.shape[1] for img in strips)
        max_height = max(img.shape[0] for img in strips)
        print(f"[Dry Run] Loaded {len(strips)} strips.")
        print(f"[Dry Run] Final stitched image size would be: {max_height}px height × {total_width}px width")
    else:
        result = stitch_images(images=strips)
        cv2.imwrite(args.output, result)
        print(f"✅ Saved stitched image to {args.output}")

if __name__ == "__main__":
    main()

