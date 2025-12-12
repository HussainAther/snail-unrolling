import numpy as np
import pytest
from capture.extractor import extract_strip, extract_center_strip, crop_center

def test_extract_strip_returns_array():
    img = np.ones((100, 100, 3), dtype=np.uint8) * 255
    center = (50, 50)
    result = extract_strip(img, center, width=10)
    assert result.ndim == 3
    assert result.shape[1] == 10  # width

def test_extract_center_strip_returns_array():
    img = np.ones((100, 100, 3), dtype=np.uint8) * 255
    result = extract_center_strip(img, width=10)
    assert result.shape[1] == 10

def test_crop_center_output_shape():
    img = np.ones((100, 100, 3), dtype=np.uint8)
    center = (50, 50)
    cropped = crop_center(img, center, size=(20, 20))
    assert cropped.shape == (20, 20, 3)

