# src/processing/extractor.py

import cv2
import numpy as np
import os

def extract_closest_strip(image_path, output_path=None, debug=False):
    """
    Extract the strip (slice) closest to the camera from a snail shell image.
    
    Parameters:
        image_path (str): Path to the input image.
        output_path (str): Path to save the extracted strip (optional).
        debug (bool): If True, print debug info and optionally visualize.
    
    Returns:
        extracted (np.ndarray): The cropped or processed image strip.
    """
    if debug:
        print(f"[extractor] Loading image: {image_path}")
        
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Image not found: {image_path}")

    # Example logic — customize this based on how your snails appear
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        raise ValueError(f"No contours found in image: {image_path}")

    # Take the largest contour (presumed snail shell)
    largest = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(largest)
    extracted = img[y:y+h, x:x+w]

    if output_path:
        cv2.imwrite(output_path, extracted)
        if debug:
            print(f"[extractor] Saved extracted strip to {output_path}")

    return extracted

