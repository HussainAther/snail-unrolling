# src/axis_detection/axis_finder.py

import cv2
import numpy as np

def detect_shell_axis(image, debug=False):
    """
    Detect the spiral center and orientation of a snail shell in an image.
    
    Returns:
        center (tuple): (x, y) pixel coordinates of spiral center
        orientation (float): rotation angle in degrees
        contour (ndarray): the largest shell-like contour (optional)
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)

    # Edge detection
    edges = cv2.Canny(blurred, 50, 150)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        raise ValueError("No contours found.")

    # Take the largest contour (assuming it's the shell)
    largest = max(contours, key=cv2.contourArea)
    (x, y), radius = cv2.minEnclosingCircle(largest)
    center = (int(x), int(y))

    # Use PCA to determine orientation
    data_pts = np.array(largest, dtype=np.float64).reshape(-1, 2)
    mean, eigenvectors = cv2.PCACompute(data_pts, mean=None, maxComponents=2)
    angle = np.arctan2(eigenvectors[0,1], eigenvectors[0,0]) * (180.0 / np.pi)

    if debug:
        debug_img = image.copy()
        cv2.circle(debug_img, center, int(radius), (0, 255, 0), 2)
        cv2.drawContours(debug_img, [largest], -1, (255, 0, 0), 1)
        cv2.imshow("Axis Detection Debug", debug_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return center, angle, largest

# Example usage
if __name__ == "__main__":
    img_path = "data/raw/snail_001.jpg"
    image = cv2.imread(img_path)
    center, angle, _ = detect_shell_axis(image, debug=True)
    print(f"Center: {center}, Rotation Angle: {angle:.2f} degrees")

