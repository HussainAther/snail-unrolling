#!/usr/bin/env python3
import sys
import os

# Add src/ to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from processing.extractor import extract_closest_strip
from mosaicing.stitcher import stitch_images

from axis_detection.axis_finder import find_spiral_axis
from projection.flatten import flatten_snail


def process_snail_folder(folder_path: str, output_dir: str, verbose: bool = False):
    from processing.extractor import extract_closest_strip
    from mosaicing.stitcher import stitch_images
    from axis_detection.axis_finder import find_spiral_axis
    from projection.flatten import flatten_shell
    import cv2

    image_files = sorted([
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if f.lower().endswith(('.jpg', '.jpeg', '.png'))
    ])

    if not image_files:
        if verbose:
            print(f"⚠️  No image files found in {folder_path}")
        return

    if verbose:
        print(f"🖼️  Found {len(image_files)} images")

    strips = [extract_closest_strip(cv2.imread(f)) for f in image_files]
    stitched = stitch_images(strips)
    axis = find_spiral_axis(stitched)
    flattened = flatten_shell(stitched, axis)

    out_path = os.path.join(output_dir, os.path.basename(folder_path) + "_unrolled.png")
    cv2.imwrite(out_path, flattened)

    if verbose:
        print(f"✅ Saved unrolled image to {out_path}")


def main():
    parser = argparse.ArgumentParser(description="Batch unroll snail images from multiple folders.")
    parser.add_argument("--input_root", required=True, help="Root directory containing folders of snail images")
    parser.add_argument("--output_dir", required=True, help="Where to save unrolled output images")
    parser.add_argument("--verbose", action="store_true", help="Print detailed progress")

    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    for subfolder in os.listdir(args.input_root):
        full_path = os.path.join(args.input_root, subfolder)
        if os.path.isdir(full_path):
            if args.verbose:
                print(f"\n📁 Processing: {subfolder}")
            process_snail_folder(full_path, args.output_dir, verbose=args.verbose)


if __name__ == "__main__":
    main()

