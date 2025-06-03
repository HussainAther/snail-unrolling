import argparse
import os
import cv2
from src.analysis.injury_analysis import compare_shell_segments, save_ssim_result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare unrolled snail shell patterns before and after injury")
    parser.add_argument("--before", required=True, help="Path to unrolled shell image before injury")
    parser.add_argument("--after", required=True, help="Path to unrolled shell image after injury")
    parser.add_argument("--no-show", action="store_true", help="Suppress SSIM heatmap display")
    parser.add_argument("--save-json", default="ssim_result.json", help="Path to save SSIM score output as JSON")
    parser.add_argument("--save-diff", default="diff_output.png", help="Path to save SSIM heatmap image")

    args = parser.parse_args()

    score, diff = compare_shell_segments(
        before_path=args.before,
        after_path=args.after,
        show=not args.no_show
    )

    print(f"SSIM Score: {score:.4f}")

    # Make output directory
    os.makedirs("log_output", exist_ok=True)

    # Save heatmap difference image
    if diff is not None:
        diff_path = os.path.join("log_output", args.save_diff)
        cv2.imwrite(diff_path, diff)
        print(f"Saved SSIM heatmap to {diff_path}")

    # Save SSIM score to JSON
    save_ssim_result(
        score=score,
        before_path=args.before,
        after_path=args.after,
        output_path=os.path.join("log_output", args.save_json)
    )

