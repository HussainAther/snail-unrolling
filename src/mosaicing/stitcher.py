# src/mosaicing/stitcher.py

import cv2
import logging
import numpy as np
import os
logger = logging.getLogger(__name__)


def stitch_strips(strips, matcher_type="ORB"):
    """
    Stitch a list of narrow image strips horizontally.
    """
    if not strips or len(strips) < 2:
        raise ValueError("Need at least two image strips to stitch.")

    # Choose feature detector
    if matcher_type == "SIFT":
        detector = cv2.SIFT_create()
    else:
        detector = cv2.ORB_create()

    base_img = strips[0]
    for i in range(1, len(strips)):
        next_img = strips[i]
        
        # Detect keypoints and descriptors
        kp1, des1 = detector.detectAndCompute(base_img, None)
        kp2, des2 = detector.detectAndCompute(next_img, None)

        if des1 is None or des2 is None:
            print(f"Skipping pair {i-1}–{i} due to no descriptors.")
            continue

        # Brute Force matcher
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(des1, des2)
        matches = sorted(matches, key=lambda x: x.distance)

        if len(matches) < 4:
            print(f"Insufficient matches for pair {i-1}–{i}. Skipping.")
            continue

        # Get matching keypoints
        src_pts = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1,1,2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1,1,2)

        # Compute homography
        H, mask = cv2.findHomography(dst_pts, src_pts, cv2.RANSAC, 5.0)

        # Warp the next image
        h1, w1 = base_img.shape[:2]
        h2, w2 = next_img.shape[:2]
        result = cv2.warpPerspective(next_img, H, (w1 + w2, max(h1, h2)))
        result[0:h1, 0:w1] = base_img

        # Update base_img
        base_img = result

    return base_img

def save_output(image, output_path, filename="stitched_strip.png"):
    """
    Save the final stitched image.
    """
    os.makedirs(output_path, exist_ok=True)
    cv2.imwrite(os.path.join(output_path, filename), image)

def load_strips(
    folder_path, 
    image_exts=(".png", ".jpg", ".jpeg"), 
    fail_on_error=False,
    verbose=True
):
    """
    Load image strips from a folder and return them as a list of numpy arrays.

    Args:
        folder_path (str): Path to folder containing image files.
        image_exts (tuple): Allowed image file extensions.
        fail_on_error (bool): If True, raise an error on failed image read.
        verbose (bool): If True, print warnings for unreadable files.

    Returns:
        list of np.ndarray: Loaded images.
    """
    strips = []
    for filename in sorted(os.listdir(folder_path)):
        if filename.lower().endswith(image_exts):
            path = os.path.join(folder_path, filename)
            img = cv2.imread(path)
            if img is None:
                logger.warning(f"Could not read image: {path}")                
            strips.append(img)
    return strips


def stitch_images(images=None, strips_folder="data/processed"):
    """
    Stitch a list of images horizontally. If no images are provided, load from folder.
    """
    if images is None:
    images = load_strips(strips_folder)

    first_height = images[0].shape[0]
    for idx, img in enumerate(images):
        if img.shape[0] != first_height:
            logger.error(f"Image at index {idx} has mismatched height: {img.shape[0]} (expected {first_height})")
            raise ValueError("All images must have the same height for horizontal stitching.")

    # Proceed with stitching
    total_width = sum(img.shape[1] for img in images)
    max_height = max(img.shape[0] for img in images)

    result = np.zeros((max_height, total_width, 3), dtype=np.uint8)

    first_height = images[0].shape[0]
    for idx, img in enumerate(images):
        if img.shape[0] != first_height:
            logger.error(f"Image at index {idx} has mismatched height: {img.shape[0]} (expected {first_height})")
            raise ValueError("All images must have the same height for horizontal stitching.")

    current_x = 0
    for img in images:
        result[:img.shape[0], current_x:current_x + img.shape[1]] = img
        current_x += img.shape[1]

    return result



if __name__ == "__main__":
    stitch_images()
