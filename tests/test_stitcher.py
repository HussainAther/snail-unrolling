import numpy as np
import pytest
from mosaicing.stitcher import stitch_images

def test_stitch_images_returns_correct_shape():
    img1 = np.ones((100, 100, 3), dtype=np.uint8) * 255
    img2 = np.zeros((100, 100, 3), dtype=np.uint8)
    result = stitch_images([img1, img2])
    assert result.shape[0] == 100
    assert result.shape[1] == 200  # stitched horizontally
    assert result.shape[2] == 3

