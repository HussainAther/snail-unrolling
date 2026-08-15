import argparse
import os
import cv2
from mosaicing.stitcher import stitch_images


def main():
    parser = argparse.ArgumentParser(description="Stitch images into a mosaic.")
    parser.add_argument(
        '--folder',
        type=str,
        default="data/processed",
        help="Folder containing input strip images"
    )
    parser.add_argument(
        '--output',
        type=str,
        default="stitched_output.png",
        help="Path to save stitched image (e.g., output/mosaic.png)"
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help="Print stitched image info without saving"
    )

    args = parser.parse_args()

    # Stitch the images
    result = stitch_images(strips_folder=args.folder)

    if args.dry_run:
        print(f"[DRY RUN] ✅ Stitched image shape: {result.shape}")
        print(f"[DRY RUN] Would save to: {args.output}")
        return

    # Ensure output directory exists
    output_dir = os.path.dirname(args.output)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    # Save the stitched image
    cv2.imwrite(args.output, result)
    print(f"✅ Stitched image saved to: {args.output}")


if __name__ == "__main__":
    main()

