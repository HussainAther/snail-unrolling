import numpy as np
from src.analysis.injury_analysis import compare_shell_segments
import cv2

def test_ssim_same_image():
    img = np.ones((256, 256), dtype=np.uint8) * 128
    cv2.imwrite("temp.png", img)
    score, _ = compare_shell_segments("temp.png", "temp.png", show=False)
    assert abs(score - 1.0) < 1e-6

