# Makefile for Snail Unrolling Project 🐌➡️📜

# Paths
BEFORE_IMG = data/processed/unrolled_snail_before.png
AFTER_IMG  = data/processed/unrolled_snail_after.png
INPUT_ROOT = data/raw
OUTPUT_DIR = outputs
PYTHON     = python

.PHONY: help extract stitch axis flatten turing ca compare run clean batch test format

all: extract stitch axis flatten

help:
	@echo ""
	@echo "🐌 Snail Unrolling Project Commands:"
	@echo "  make extract       - Extract strips from raw shell images"
	@echo "  make stitch        - Stitch strips into a mosaic"
	@echo "  make axis          - Detect spiral axis from stitched image"
	@echo "  make flatten       - Flatten the shell image into 2D"
	@echo "  make turing        - Run Gray-Scott simulation from config"
	@echo "  make ca            - Generate and plot a cellular automaton"
	@echo "  make compare       - Compare before/after injury patterns"
	@echo "  make run           - Generate + compare using CLI script"
	@echo "  make batch         - Batch unroll all snails from raw folders"
	@echo "  make test          - Run unit tests"
	@echo "  make format        - Format code using Black"
	@echo "  make clean         - Remove generated images"
	@echo ""

setup:
	python -m venv venv && source venv/bin/activate && pip install -r requirements.txt

extract:
	$(PYTHON) src/capture/extractor.py

stitch:
	$(PYTHON) src/mosaicing/stitcher.py

axis:
	$(PYTHON) src/axis_detection/axis_finder.py

flatten:
	$(PYTHON) src/projection/flatten.py

turing:
	$(PYTHON) run_gray_scott.py --config config/config.yaml --show

ca:
	$(PYTHON) src/modeling/cellular_automata.py

compare:
	$(PYTHON) src/analysis/injury_analysis.py

run:
	$(PYTHON) run_injury_analysis.py --save_before $(BEFORE_IMG) --save_after $(AFTER_IMG) --perturb --compare

batch:
	PYTHONPATH=. $(PYTHON) scripts/batch_unroll.py --input_root $(INPUT_ROOT) --output_dir $(OUTPUT_DIR) --verbose


test:
	pytest tests/

format:
	black src/ scripts/ tests/

clean:
	rm -f $(BEFORE_IMG) $(AFTER_IMG) pattern_comparison.png
	rm -rf $(OUTPUT_DIR)/*.png
	rm -f data/stitched/*.png
