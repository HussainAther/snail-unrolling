import numpy as np
import cv2
import tempfile
import os

from capture.extractor import extract_closest_strip


def test_extract_closest_strip_shape():
    """Ensure extracted strip has expected dimensions."""
    img = np.zeros((100, 200, 3), dtype=np.uint8)

    strip = extract_closest_strip(img, strip_width=20)

    assert strip is not None
    assert strip.shape[0] == 100
    assert strip.shape[1] == 20
    assert strip.shape[2] == 3


def test_extract_closest_strip_values():
    """Ensure strip actually comes from image center."""
    img = np.zeros((100, 200, 3), dtype=np.uint8)
    img[:, 90:110] = 255  # bright vertical band

    strip = extract_closest_strip(img, strip_width=20)

    assert strip.mean() > 200

