# src/capture/extractor.py

import cv2
import numpy as np
import os

def load_images_from_folder(folder_path, image_exts=[".jpg", ".png", ".jpeg"]):
    """
    Load all images from a specified folder with given extensions.
    """
    images = []
    for filename in sorted(os.listdir(folder_path)):
        if any(filename.lower().endswith(ext) for ext in image_exts):
            img_path = os.path.join(folder_path, filename)
            image = cv2.imread(img_path)
            if image is not None:
                images.append(image)
    return images

def extract_narrow_strip(image, strip_height_ratio=0.1):
    """
    Extract a narrow horizontal strip from the vertical center of an image.
    
    Parameters:
        image (ndarray): Input image (H x W x 3)
        strip_height_ratio (float): Percentage height of strip to extract
    Returns:
        strip (ndarray): Cropped strip
    """
    height, width = image.shape[:2]
    strip_height = int(height * strip_height_ratio)
    y_start = height // 2 - strip_height // 2
    y_end = y_start + strip_height
    strip = image[y_start:y_end, :]
    return strip

def save_strip(strip, output_path, filename):
    """
    Save the extracted strip as an image.
    """
    os.makedirs(output_path, exist_ok=True)
    save_path = os.path.join(output_path, filename)
    cv2.imwrite(save_path, strip)

def process_folder(input_folder, output_folder, strip_height_ratio=0.1):
    """
    Full pipeline to load images, extract strips, and save them.
    """
    images = load_images_from_folder(input_folder)
    for idx, img in enumerate(images):
        strip = extract_narrow_strip(img, strip_height_ratio)
        save_strip(strip, output_folder, f"strip_{idx:03}.png")

# Example usage (comment out if using as a module)
if __name__ == "__main__":
    input_folder = "data/raw"
    output_folder = "data/processed"
    process_folder(input_folder, output_folder, strip_height_ratio=0.08)

