import os
import cv2
import numpy as np
from pathlib import Path

# Settings
output_dir = "data/raw/snail_001"  # Adjust path if needed
os.makedirs(output_dir, exist_ok=True)

# Parameters
image_size = 512
center = (image_size // 2, image_size // 2)
radius = 200
num_images = 36

# Generate spiral-like patterns
for i in range(num_images):
    angle = 2 * np.pi * i / num_images
    image = np.ones((image_size, image_size, 3), dtype=np.uint8) * 255

    for t in np.linspace(0, 4 * np.pi, 1000):
        r = radius * t / (4 * np.pi)
        x = int(center[0] + r * np.cos(t + angle))
        y = int(center[1] + r * np.sin(t + angle))
        if 0 <= x < image_size and 0 <= y < image_size:
            image[y, x] = (80, 30, 200)

    cv2.imwrite(os.path.join(output_dir, f"view_{i:04d}.png"), image)

print(f"✅ Generated {num_images} mock snail images in {output_dir}")

