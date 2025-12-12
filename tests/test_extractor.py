# tests/test_extractor.py

import numpy as np
import cv2
from src.extractor import extract_closest_strip

def test_extract_closest_strip():
    img = np.ones((100, 100, 3), dtype=np.uint8) * 255  # White image
    center = (50, 50)
    strip = extract_closest_strip(img, center=center, width=5)

    assert strip is not None
    assert strip.shape[0] == img.shape[0]  # height
    assert strip.shape[1] == 5  # width
    assert strip.shape[2] == 3  # RGB

