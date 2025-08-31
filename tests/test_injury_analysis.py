import cv2
import numpy as np
import pytest
from src.analysis.injury_analysis import compare_shell_segments

def test_ssim_mismatched_shapes(tmp_path):
    # Create two dummy images with different shapes
    img1 = np.ones((256, 256), dtype=np.uint8) * 120
    img2 = np.ones((300, 300), dtype=np.uint8) * 120

    path1 = tmp_path / "img1.png"
    path2 = tmp_path / "img2.png"
    cv2.imwrite(str(path1), img1)
    cv2.imwrite(str(path2), img2)

    # Expect the function to raise an error due to shape mismatch
    with pytest.raises(ValueError):
        compare_shell_segments(str(path1), str(path2), show=False)

