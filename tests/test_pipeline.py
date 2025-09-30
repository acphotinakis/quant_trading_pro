#!/usr/bin/env python3
"""
Data Pipeline Tests
Phase 2: Data Acquisition & Infrastructure
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import sys
import os

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from data.validation import DataValidator
from data.pipeline import DataPipeline


class TestDataPipeline:
    def test_pipeline_initialization(self):
        """Test that pipeline initializes correctly"""
        pipeline = DataPipeline()
        assert pipeline is not None
        assert hasattr(pipeline, "logger")
        assert hasattr(pipeline, "config")

    def test_rate_limiting(self):
        """Test rate limiting functionality"""
        pipeline = DataPipeline()
        # This is a basic test - actual rate limiting would be tested with integration tests
        assert "yfinance" in pipeline.providers or "alpaca" in pipeline.providers

    def test_data_validation(self):
        """Test data validation functionality"""
        validator = DataValidator()

        # Create test data
        test_data = pd.DataFrame(
            {
                "open": [100, 101, 102],
                "high": [105, 106, 107],
                "low": [95, 96, 97],
                "close": [102, 103, 104],
                "volume": [1000000, 1200000, 1100000],
            },
            index=pd.date_range("2024-01-01", periods=3, freq="D"),
        )

        results = validator.validate_ohlcv_data(test_data, "TEST")
        assert results["checks_passed"] > 0
        assert "ticker" in results


class MockDataProvider:
    """Mock data provider for testing"""

    @staticmethod
    def fetch_ohlcv(ticker, start_date, end_date):
        return pd.DataFrame(
            {
                "open": [100, 101],
                "high": [105, 106],
                "low": [95, 96],
                "close": [102, 103],
                "volume": [1000000, 1200000],
            },
            index=pd.date_range("2024-01-01", periods=2, freq="D"),
        )


def test_mock_data_provider():
    """Test with mock data provider"""
    provider = MockDataProvider()
    data = provider.fetch_ohlcv("TEST", "2024-01-01", "2024-01-02")
    assert len(data) == 2
    assert all(
        col in data.columns for col in ["open", "high", "low", "close", "volume"]
    )


if __name__ == "__main__":
    # Run basic tests
    test_pipeline = TestDataPipeline()
    test_pipeline.test_pipeline_initialization()
    test_pipeline.test_data_validation()
    test_mock_data_provider()
    print("✅ All Phase 2 tests passed")
