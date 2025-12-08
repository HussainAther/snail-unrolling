# src/mosaicing/stitcher.py

import cv2
import numpy as np
import os

def load_strips(folder_path, image_exts=[".png", ".jpg", ".jpeg"]):
    """
    Load cropped strip images in order.
    """
    strips = []
    for filename in sorted(os.listdir(folder_path)):
        if any(filename.lower().endswith(ext) for ext in image_exts):
            img_path = os.path.join(folder_path, filename)
            img = cv2.imread(img_path)
            if img is not None:
                strips.append(img)
    return strips

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

def stitch_images():
    """
    Stitch the images together.
    """
    strips_folder = "data/processed"
    output_folder = "data/stitched"
    
    strips = load_strips(strips_folder)
    stitched_image = stitch_strips(strips, matcher_type="ORB")
    save_output(stitched_image, output_folder)

if __name__ == "__main__":
    stitch_images()
