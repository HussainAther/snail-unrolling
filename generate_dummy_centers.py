import os
import json

raw_root = "data/raw"
center = {"x": 256, "y": 256}

for subfolder in os.listdir(raw_root):
    path = os.path.join(raw_root, subfolder)
    if os.path.isdir(path):
        with open(os.path.join(path, "axis.json"), "w") as f:
            json.dump(center, f)
        print(f"✅ Created axis.json in {subfolder}")

