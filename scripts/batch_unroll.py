import os
import argparse
from src.processing.extractor import extract_closest_strip
from src.processing.flatten import build_unrolled_projection
import cv2


def process_snail_folder(folder_path, output_dir, verbose=False):
    # Sort all image files numerically
    image_files = sorted(
        [f for f in os.listdir(folder_path) if f.lower().endswith((".png", ".jpg", ".jpeg"))],
        key=lambda x: int(os.path.splitext(x)[0])
    )
    strips = []

    for filename in image_files:
        img_path = os.path.join(folder_path, filename)
        image = cv2.imread(img_path)
        if image is None:
            if verbose:
                print(f"Warning: Skipping unreadable image {img_path}")
            continue

        strip = extract_closest_strip(image)
        strips.append(strip)

    if strips:
        unrolled = build_unrolled_projection(strips)
        snail_name = os.path.basename(folder_path.rstrip("/"))
        output_path = os.path.join(output_dir, f"{snail_name}_unrolled.png")
        cv2.imwrite(output_path, unrolled)
        if verbose:
            print(f"✅ Saved unrolled image to: {output_path}")
    else:
        if verbose:
            print(f"⚠️ No valid images found in: {folder_path}")


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

