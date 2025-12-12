import numpy as np
import cv2
import pytest
from axis_detection.axis_finder import find_spiral_axis

def test_find_spiral_axis_returns_tuple():
    dummy_image = np.zeros((100, 100, 3), dtype=np.uint8)
    center = find_spiral_axis(dummy_image)
    assert isinstance(center, tuple)
    assert len(center) == 2
    assert all(isinstance(coord, int) for coord in center)

