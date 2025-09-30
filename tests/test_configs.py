"""
Configuration Validation Tests
Phase 1: Research & Scoping
"""

import yaml
import pytest
from pathlib import Path


def test_config_files_exist():
    """Test that all required config files exist"""
    required_files = [
        "config/success_metrics.yaml",
        "config/system_limits.yaml",
        "config/regime_definitions.yaml",
    ]

    for file_path in required_files:
        assert Path(file_path).exists(), f"Missing config file: {file_path}"


def test_yaml_syntax():
    """Test that all YAML files are syntactically valid"""
    config_files = list(Path("config").glob("*.yaml"))

    for config_file in config_files:
        try:
            with open(config_file, "r") as f:
                yaml.safe_load(f)
        except yaml.YAMLError as e:
            pytest.fail(f"Invalid YAML in {config_file}: {e}")


def test_success_metrics_structure():
    """Test success metrics configuration structure"""
    with open("config/success_metrics.yaml", "r") as f:
        config = yaml.safe_load(f)

    assert "metrics" in config
    assert "primary" in config["metrics"]
    assert "secondary" in config["metrics"]
    assert "regime_requirements" in config

    # Test primary metrics exist
    primary_metrics = config["metrics"]["primary"]
    assert "information_coefficient" in primary_metrics
    assert "sharpe_ratio" in primary_metrics


def test_system_limits_structure():
    """Test system limits configuration structure"""
    with open("config/system_limits.yaml", "r") as f:
        config = yaml.safe_load(f)

    required_sections = ["compute", "storage", "api", "constraints"]
    for section in required_sections:
        assert section in config, f"Missing section: {section}"


def test_regime_definitions_structure():
    """Test regime definitions configuration structure"""
    with open("config/regime_definitions.yaml", "r") as f:
        config = yaml.safe_load(f)

    assert "regime_indicators" in config
    assert "regime_classification" in config

    # Test VIX thresholds exist
    vix_config = config["regime_indicators"]["vix"]
    assert "thresholds" in vix_config
    assert "low_vol" in vix_config["thresholds"]
    assert "high_vol" in vix_config["thresholds"]


if __name__ == "__main__":
    # Run tests
    test_config_files_exist()
    test_yaml_syntax()
    test_success_metrics_structure()
    test_system_limits_structure()
    test_regime_definitions_structure()
    print("✓ All configuration tests passed")
