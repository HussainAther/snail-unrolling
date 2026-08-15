# src/mosaicing/stitcher.py

import cv2
import os
import numpy as np

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
                msg = f"[WARN] Could not read image: {path}"
                if fail_on_error:
                    raise IOError(msg)
                elif verbose:
                    print(msg)
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

    result = np.zeros((max_height, total_width, 3), dtype=np.uint8)

    current_x = 0
    for img in images:
        result[:img.shape[0], current_x:current_x + img.shape[1]] = img
        current_x += img.shape[1]

    return result



if __name__ == "__main__":
    stitch_images()
