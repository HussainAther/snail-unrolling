## 🐌 Snail Unrolling – Computational Mosaicing & Pattern Analysis

Unroll the complex 3D spiral of a snail shell into a 2D map for analysis, pattern modeling, and biological insight. Inspired by discussions with Dick Gordon, this project investigates the mechanisms of shell growth, damage recovery, and pigmentation pattern formation.

---

### 🚀 Features
- 🌀 **Extract**: Narrow strip extraction from shell images
- 🧩 **Stitch**: Mosaicing of shell strips into a full panoramic view
- 🧭 **Axis Detection**: Identify spiral center and orientation
- 🗺 **Flatten**: Project spiral surface into a 2D plane (“Unrolling the Snail”)
- 🎨 **Simulate**: Generate synthetic shell patterns with Turing and Cellular Automata models
- 🩹 **Compare**: Analyze pre-/post-injury shell patterns for damage recovery and modeling validation
- ✅ **Command-Line Ready** with Makefile + CLI scripting

---

### 📁 Project Structure
```
snail-unrolling/
├── data/
│   ├── raw/                      ← Raw snail shell images
│   └── processed/                ← Processed strips, flattened outputs
├── src/
│   ├── capture/
│   │   └── extractor.py          ← Extract strips from 360° shell images
│   ├── mosaicing/
│   │   └── stitcher.py           ← Mosaicing with ORB/SIFT
│   ├── axis_detection/
│   │   └── axis_finder.py        ← Spiral axis + orientation detection
│   ├── projection/
│   │   └── flatten.py            ← Polar projection to 2D unrolled map
│   ├── modeling/
│   │   ├── turing.py             ← Reaction-diffusion pattern simulator
│   │   └── cellular_automata.py  ← 1D cellular automaton pattern generator
│   ├── analysis/
│   │   └── injury_analysis.py    ← SSIM comparison of shell before/after injury
│   └── utils/
│       └── image_utils.py        ← (Optional) Image resizing, normalization
├── run_injury_analysis.py        ← CLI tool for simulating + comparing patterns
├── pattern_analysis.py           ← Demo/plotting script for comparing patterns
├── requirements.txt
├── Makefile                      ← Easy command-line interface
├── .gitignore
└── README.md
```

---

### 🛠️ Usage

#### 🔧 Install dependencies:
```bash
pip install -r requirements.txt
```

#### 🐌 Run full CLI pattern pipeline:
```bash
make run
```

#### 🛠 Other CLI tasks:
```bash
make extract     # Strip from raw images
make stitch      # Mosaic them
make axis        # Detect shell axis
make flatten     # Flatten into 2D
make turing      # Simulate Turing pattern
make ca          # Simulate cellular automata
make compare     # Run injury comparison
make clean       # Delete generated outputs
```

---

### 🧠 Why Turing & Cellular Automata?

Snail shell patterns aren’t random — they arise from dynamic biological processes:

- **Turing Patterns** (reaction-diffusion systems) simulate morphogen-based pigment regulation
- **Cellular Automata** simulate discrete rule-based development, reflecting genetic control systems

Both models allow us to test biological hypotheses — especially in **injury recovery**, where regenerated patterns may reveal deeper properties of developmental stability and error correction.

---

### 🩹 Shell Injury Recovery Hypothesis

Injured shells that regenerate offer a **natural experiment**:  
> Does the snail “replay” the same rules to rebuild its pattern?

By comparing pre- and post-injury segments, we can test whether **patterning logic is resilient**, disrupted, or adaptive — helping understand both normal growth and developmental plasticity.


# 🐌 Snail Unrolling Pattern Analysis

## Usage Examples

### 1. Run Shell Projection
```bash
python src/projection/flatten.py --image data/raw/shell.jpg --cx 300 --cy 300 --output data/processed/unrolled_snail.png
```

### 2. Compare Before/After Injury Shells
```bash
python run_injury_analysis.py \
  --before data/processed/unrolled_snail_before.png \
  --after data/processed/unrolled_snail_after.png \
  --no-show \
  --save-json ssim_result.json \
  --save-diff diff_map.png
```

### 3. Generate a Turing Pattern
```bash
python generate_turing.py
# Output saved to: turing_pattern.png
```

### 4. Run Full Analysis Pipeline (WIP)
```bash
python pipeline/analyze_folder.py --input-folder data/processed/snail_pairs
```

## More Info
See CONTRIBUTING.md and photo_checklist.md for how to help and contribute.

---

### 💡 Credits

Developed in collaboration with ideas and guidance from **Dick Gordon**.  
Maintained by an interdisciplinary team blending neurodiversity, computational biology, and machine learning.


