import cv2
import os

def load_images_from_folder(folder, exts=[".jpg", ".png"]):
    images = []
    for file in sorted(os.listdir(folder)):
        if any(file.lower().endswith(ext) for ext in exts):
            images.append(cv2.imread(os.path.join(folder, file)))
    return images

