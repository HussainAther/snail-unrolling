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

