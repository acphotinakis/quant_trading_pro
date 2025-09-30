"""
Quant Trading Pro - Repository Initialization Script
Phase 1: Research & Scoping
"""

import os
import sys
import yaml
import logging
from pathlib import Path
from datetime import datetime


def setup_logging():
    """Initialize logging for setup process"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_dir / "setup.log"),
            logging.StreamHandler(sys.stdout),
        ],
    )
    return logging.getLogger(__name__)


def validate_config_files(logger):
    """Validate all YAML configuration files"""
    config_files = [
        "config/success_metrics.yaml",
        "config/system_limits.yaml",
        "config/regime_definitions.yaml",
    ]

    for config_file in config_files:
        if not Path(config_file).exists():
            logger.error(f"Missing config file: {config_file}")
            return False

        try:
            with open(config_file, "r") as f:
                yaml.safe_load(f)
            logger.info(f"✓ Validated: {config_file}")
        except yaml.YAMLError as e:
            logger.error(f"Invalid YAML in {config_file}: {e}")
            return False

    return True


def create_folder_structure(logger):
    """Create the complete folder structure"""
    folders = [
        # Data directories
        "data/universe",
        "data/regimes",
        "data/raw",
        "data/processed",
        "data/backtests",
        "data/validation",
        "data/models",
        # Source code directories
        "src/data",
        "src/features",
        "src/models",
        "src/execution",
        "src/backtesting",
        "src/validation",
        "src/monitoring",
        "src/regimes",
        "src/utils",
        # Script directories
        "scripts/setup",
        "scripts/deployment",
        "scripts/analysis",
        "scripts/monitoring",
        # Test directories
        "tests/unit",
        "tests/integration",
        "tests/performance",
        "tests/fixtures",
        # Other directories
        "logs",
        "plots",
        "reports",
        "docs",
    ]

    for folder in folders:
        Path(folder).mkdir(parents=True, exist_ok=True)
        logger.info(f"Created: {folder}")


def main():
    """Main setup function"""
    logger = setup_logging()
    logger.info("Starting Quant Trading Pro - Phase 1 Setup")

    try:
        # Create folder structure
        logger.info("Creating folder structure...")
        create_folder_structure(logger)

        # Validate configuration files
        logger.info("Validating configuration files...")
        if not validate_config_files(logger):
            raise Exception("Configuration validation failed")

        # Create checkpoint file
        checkpoint = {
            "phase": 1,
            "step": "repo_initialization",
            "timestamp": datetime.now().isoformat(),
            "status": "completed",
        }

        with open("logs/setup_checkpoint.json", "w") as f:
            json.dump(checkpoint, f, indent=2)

        logger.info("✓ Phase 1 setup completed successfully")

    except Exception as e:
        logger.error(f"Setup failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
