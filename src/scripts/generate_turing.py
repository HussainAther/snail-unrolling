import argparse
import cv2
from src.modeling.turing import run_gray_scott


def save_pattern_image(U, V=None, output_path="turing_pattern.png", output_path_v=None):
    img_u = (U * 255).astype("uint8")
    cv2.imwrite(output_path, img_u)
    print(f"Turing U pattern saved to {output_path}")

    if V is not None and output_path_v:
        img_v = (V * 255).astype("uint8")
        cv2.imwrite(output_path_v, img_v)
        print(f"Turing V pattern saved to {output_path_v}")


def main():
    parser = argparse.ArgumentParser(description="Generate and save a Turing pattern image")
    parser.add_argument("--steps", type=int, default=5000, help="Number of simulation steps")
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility")
    parser.add_argument("--output", type=str, default="turing_pattern.png", help="Output image path for U")
    parser.add_argument("--output_v", type=str, default=None, help="Optional output image path for V")
    parser.add_argument("--show", action="store_true", help="Display pattern in a window")
    parser.add_argument("--config", type=str, help="Optional YAML config file")
    args = parser.parse_args()

    # Load config overrides
    if args.config:
        from src.utils.config_loader import load_config
        cfg = load_config(args.config)
        args.steps = cfg.get("steps", args.steps)
        args.seed = cfg.get("seed", args.seed)
        args.output = cfg.get("output", args.output)
        args.output_v = cfg.get("output_v", args.output_v)

    U, V = run_gray_scott(steps=args.steps, seed=args.seed)
    save_pattern_image(U, V, args.output, args.output_v)

    if args.show:
        cv2.imshow("Turing U", (U * 255).astype("uint8"))
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

