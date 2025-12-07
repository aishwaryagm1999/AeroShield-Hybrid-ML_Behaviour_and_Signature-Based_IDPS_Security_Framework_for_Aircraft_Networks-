#!/usr/bin/env bash
set -e

echo "[*] Running full model update pipeline..."
python -m src.maintenance.model_update_pipeline
