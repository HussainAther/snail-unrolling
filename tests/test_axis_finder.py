# tests/test_axis_finder.py

import numpy as np
from src.axis_detection.axis_finder import find_spiral_axis

def test_find_spiral_axis_returns_center():
    dummy_img = np.zeros((400, 400, 3), dtype=np.uint8)
    center = find_spiral_axis(dummy_img)
    
    assert isinstance(center, tuple)
    assert len(center) == 2
    assert all(isinstance(c, int) for c in center)

