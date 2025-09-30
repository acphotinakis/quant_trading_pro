# scripts/phase2_setup.py
import yaml
import pandas as pd
from pathlib import Path
import logging
import sys


def validate_phase1_artifacts():
    """Validate all required Phase 1 artifacts exist"""
    required_files = [
        "docs/project_objectives.md",
        "config/success_metrics.yaml",
        "config/system_limits.yaml",
        "config/regime_definitions.yaml",
        "data/universe/sp500_constituents.csv",
        "data/regimes/initial_regime_data.parquet",
    ]

    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)

    if missing_files:
        raise FileNotFoundError(f"Missing Phase 1 artifacts: {missing_files}")

    # Validate config files are readable
    for config_file in Path("config").glob("*.yaml"):
        with open(config_file, "r") as f:
            yaml.safe_load(f)

    # Validate universe data
    universe = pd.read_csv("data/universe/sp500_constituents.csv")
    if len(universe) < 500:
        raise ValueError(f"Universe too small: {len(universe)} constituents")

    return True


# Run validation
try:
    validate_phase1_artifacts()
    print("✅ Phase 1 artifacts validated successfully")
except Exception as e:
    print(f"❌ Phase 1 validation failed: {e}")
    sys.exit(1)
