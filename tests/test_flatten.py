import numpy as np
import pytest
from projection.flatten import polar_unroll

def test_polar_unroll_output_shape():
    img = np.ones((500, 500, 3), dtype=np.uint8) * 255
    center = (250, 250)
    unrolled = polar_unroll(img, center, output_shape=(100, 360))
    assert unrolled.shape == (100, 360, 3)

