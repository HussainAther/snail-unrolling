# src/projection/flatten.py

import cv2
import numpy as np
import math

from src.projection.flatten import unroll_shell

def unroll_shell(image, center, output_shape=(400, 720), r_min=20):
    """
    Unroll a shell image into a flat 2D polar projection.

    Parameters:
        image (ndarray): Input snail shell image
        center (tuple): (x, y) center of spiral
        output_shape (tuple): (height=radial steps, width=angle steps)
        r_min (int): Inner radius to skip overexposed center

    Returns:
        unrolled (ndarray): Unwrapped 2D image (polar to cartesian)
    """
    h, w = output_shape
    cx, cy = center
    max_radius = min(image.shape[0] - cy, image.shape[1] - cx)

    # Create empty unrolled image
    unrolled = np.zeros((h, w, 3), dtype=np.uint8)

    for i in range(h):  # radial steps
        r = r_min + (i * (max_radius - r_min) / h)
        for j in range(w):  # angle steps
            theta = 2 * math.pi * j / w
            x = int(cx + r * math.cos(theta))
            y = int(cy + r * math.sin(theta))

            if 0 <= x < image.shape[1] and 0 <= y < image.shape[0]:
                unrolled[i, j] = image[y, x]

    return unrolled

# Example usage
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", required=True, help="Input image path")
    parser.add_argument("--cx", type=int, required=True)
    parser.add_argument("--cy", type=int, required=True)
    parser.add_argument("--output", default="unrolled_output.png")
    args = parser.parse_args()

    img = cv2.imread(args.image)
    center = (args.cx, args.cy)
    result = unroll_shell(img, center)
    cv2.imwrite(args.output, result)

