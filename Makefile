# Makefile for Snail Unrolling Project 🐌➡️📜

# Default paths
BEFORE_IMG = data/processed/unrolled_snail_before.png
AFTER_IMG  = data/processed/unrolled_snail_after.png

.PHONY: help extract stitch axis flatten turing ca compare run clean

help:
	@echo ""
	@echo "🐌 Snail Unrolling Project Commands:"
	@echo "  make extract       - Extract strips from raw shell images"
	@echo "  make stitch        - Stitch strips into a mosaic"
	@echo "  make axis          - Detect spiral axis from stitched image"
	@echo "  make flatten       - Flatten the shell image into 2D"
	@echo "  make turing        - Generate and plot a Turing pattern"
	@echo "  make ca            - Generate and plot a cellular automaton"
	@echo "  make compare       - Compare before/after injury patterns"
	@echo "  make run           - Generate + compare using CLI script"
	@echo "  make clean         - Remove generated images"
	@echo ""

extract:
	python src/capture/extractor.py

stitch:
	python src/mosaicing/stitcher.py

axis:
	python src/axis_detection/axis_finder.py

flatten:
	python src/projection/flatten.py

turing:
	python src/modeling/turing.py

ca:
	python src/modeling/cellular_automata.py

compare:
	python src/analysis/injury_analysis.py

run:
	python run_injury_analysis.py --save_before $(BEFORE_IMG) --save_after $(AFTER_IMG) --perturb --compare

clean:
	rm -f data/processed/unrolled_snail_before.png
	rm -f data/processed/unrolled_snail_after.png
	rm -f pattern_comparison.png
	rm -f data/stitched/*.png

# Makefile for Snail Unrolling Project

# Default input/output paths for batch unrolling
INPUT_ROOT=data/raw
OUTPUT_DIR=outputs

# Python interpreter
PYTHON=python

# Batch unroll images from input_root and save to output_dir
batch:
	$(PYTHON) scripts/batch_unroll.py --input_root $(INPUT_ROOT) --output_dir $(OUTPUT_DIR) --verbose

# Run unit tests (if you have tests in tests/)
test:
	pytest tests/

# Format code with black
format:
	black src/ scripts/ tests/

# Run Turing pattern generator with config
turing:
	$(PYTHON) run_gray_scott.py --config config/config.yaml --show

# Clean outputs (be careful!)
clean:
	rm -rf $(OUTPUT_DIR)/*.png

# Help
help:
	@echo "Available targets:"
	@echo "  batch     - Run batch unrolling on input_root"
	@echo "  test      - Run unit tests"
	@echo "  format    - Format code using Black"
	@echo "  turing    - Run Gray-Scott simulation from config"
	@echo "  clean     - Delete all output projections"

