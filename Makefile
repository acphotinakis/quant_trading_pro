# Makefile for Quant Trading Pro

.PHONY: run

test_phase1:
	@echo "Running tests for Phase 1..."
	python3 scripts/setup/phase1_runner.py
	

test_configs:
	@echo "Running tests..."
	python3 tests/test_configs.py


initial_classification:
	@echo "Running initial regime classification..."
	python3 src/regimes/initial_classification.py


