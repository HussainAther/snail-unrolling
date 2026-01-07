# src/mosaicing/stitcher.py

import cv2
import os
import numpy as np

def load_strips(folder_path, image_exts=[".png", ".jpg", ".jpeg"]):
    strips = []
    for filename in sorted(os.listdir(folder_path)):
        if any(filename.lower().endswith(ext) for ext in image_exts):
            path = os.path.join(folder_path, filename)
            img = cv2.imread(path)
            if img is None:
                print(f"⚠️ Could not read image: {path}")
                continue
            strips.append(img)
    return strips

def stitch_images(images=None, strips_folder="data/processed"):
    if images is None:
        images = load_strips(strips_folder)
    if not images:
        raise ValueError("No images to stitch.")

    total_width = sum(img.shape[1] for img in images)
    max_height = max(img.shape[0] for img in images)

    result = np.zeros((max_height, total_width, 3), dtype=np.uint8)

    current_x = 0
    for img in images:
        result[:img.shape[0], current_x:current_x + img.shape[1]] = img
        current_x += img.shape[1]

    return result

