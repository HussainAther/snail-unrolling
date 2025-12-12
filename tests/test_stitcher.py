# tests/test_stitcher.py

import numpy as np
from src.stitcher import stitch_images

def test_stitch_images():
    strips = [np.full((100, 10, 3), fill_value=i, dtype=np.uint8) for i in range(5)]
    result = stitch_images(strips)

    assert result.shape == (100, 50, 3)  # 5 strips of width 10

