import numpy as np
import cv2
from src.analysis.injury_analysis import compare_shell_segments

def test_ssim_high_score_for_similar_images(tmp_path):
    # Create two nearly identical grayscale images
    img1 = np.ones((256, 256), dtype=np.uint8) * 180
    img2 = img1.copy()
    img2[100:110, 100:110] = 175  # Small local variation

    path1 = tmp_path / "img1.png"
    path2 = tmp_path / "img2.png"
    cv2.imwrite(str(path1), img1)
    cv2.imwrite(str(path2), img2)

    score, _ = compare_shell_segments(str(path1), str(path2), show=False)
    
    # Assert that score is high
    assert score > 0.95, f"Expected SSIM > 0.95, got {score}"

