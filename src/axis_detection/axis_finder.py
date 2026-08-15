# src/axis_detection/axis_finder.py

import cv2
import numpy as np
from typing import Tuple

def find_spiral_axis(image: np.ndarray) -> Tuple[int, int]:
    """
    Estimate the spiral axis (center point) of a snail shell image.

    This uses:
    - grayscale conversion
    - Gaussian blur
    - Hough Circle Transform to find dominant circular contour

    Returns:
        (cx, cy): estimated center of the shell spiral
    """

    if image is None:
        raise ValueError("find_spiral_axis() received empty image")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9, 9), 2)

    # Try detecting circles
    circles = cv2.HoughCircles(
        blur,
        cv2.HOUGH_GRADIENT,
        dp=1.2,
        minDist=50,
        param1=80,
        param2=30,
        minRadius=20,
        maxRadius=min(image.shape[:2]) // 2
    )

    if circles is not None:
        circles = np.uint16(np.around(circles))
        # Take the largest detected circle
        largest = max(circles[0, :], key=lambda c: c[2])
        cx, cy, _ = largest
    else:
        # Fallback: assume center of mass
        M = cv2.moments(gray)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
        else:
            # Fallback of fallback: image center
            h, w = gray.shape[:2]
            cx, cy = w // 2, h // 2

    return (cx, cy)

