#!/usr/bin/env bash
set -e

# Train models (if not already trained)
python -m src.training.train_rf_if

# Run the high-level IDS simulation
python -m src.simulation.simulate_attacks
