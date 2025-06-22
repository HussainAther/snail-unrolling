import numpy as np
import cv2
from src.projection.flatten import unroll_shell

def test_unroll_output_shape(tmp_path):
    # Create a dummy circular shell image
    size = 512
    img = np.zeros((size, size), dtype=np.uint8)
    cv2.circle(img, (size // 2, size // 2), 100, 255, -1)

    # Unroll it
    cx, cy = size // 2, size // 2
    unrolled = unroll_shell(img, center=(cx, cy), output_shape=(300, 720))

    # Test the output shape
    assert unrolled.shape == (300, 720), f"Expected shape (300, 720), got {unrolled.shape}"

