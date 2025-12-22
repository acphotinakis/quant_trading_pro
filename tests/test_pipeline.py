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
from unittest.mock import patch, MagicMock

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from data.pipeline import DataPipeline
from data.validation import DataValidator

@pytest.fixture
def pipeline(tmp_path):
    """Fixture for a DataPipeline instance with a temporary data directory."""
    # Create dummy config and universe files in a temporary directory
    data_path = tmp_path / "data"
    data_path.mkdir()
    (data_path / "universe").mkdir()
    
    # Create a dummy universe file
    dummy_universe = pd.DataFrame({
        'ticker': ['AAPL', 'GOOG', 'MSFT'],
        'company_name': ['Apple', 'Google', 'Microsoft'],
        'sector': ['Tech', 'Tech', 'Tech']
    })
    dummy_universe.to_csv(data_path / "universe" / "sp500_constituents.csv", index=False)

    # Patch the pipeline's base_path to use the temporary directory
    with patch.object(DataPipeline, 'base_path', data_path):
        pl = DataPipeline()
        yield pl

def test_pipeline_initialization(pipeline):
    """Test that pipeline initializes correctly."""
    assert pipeline is not None
    assert hasattr(pipeline, "logger")
    assert hasattr(pipeline, "config")
    assert "yfinance" in pipeline.providers

@patch('yfinance.download')
def test_smarter_top_k_selection(mock_download, pipeline):
    """Test the top-K selection based on dollar volume."""
    # Mock the yfinance download call to return predictable data
    mock_data = {
        'AAPL': pd.DataFrame({'Close': [150, 151], 'Volume': [100, 100]}),
        'GOOG': pd.DataFrame({'Close': [2800, 2810], 'Volume': [200, 200]}),
        'MSFT': pd.DataFrame({'Close': [300, 301], 'Volume': [50, 50]}),
    }
    # yfinance returns a multi-index dataframe when group_by='ticker'
    mock_df = pd.concat(mock_data.values(), keys=mock_data.keys(), names=['ticker', 'Date'])
    # Reorder columns to match yfinance output
    cols = ['Close', 'Volume']
    mock_df.columns = cols
    
    # Create a mock that can be indexed by ticker
    mock_daily_data = MagicMock()
    mock_daily_data.__getitem__.side_effect = lambda ticker: mock_data[ticker]

    mock_download.return_value = mock_daily_data

    top_2 = pipeline.select_top_k_universe(k=2)
    
    # GOOG should be first (2805 * 200 = 561000), AAPL second (150.5 * 100 = 15050)
    assert len(top_2) == 2
    assert 'GOOG' in top_2['ticker'].values
    assert 'AAPL' in top_2['ticker'].values
    assert 'MSFT' not in top_2['ticker'].values

@patch('data.pipeline.DataPipeline.fetch_ohlcv_yfinance')
@patch('data.pipeline.DataPipeline.fetch_ohlcv_alpaca')
def test_provider_fallback(mock_alpaca, mock_yfinance, pipeline):
    """Test that the fallback chain works correctly."""
    # Arrange: Alpaca fails, yfinance succeeds
    mock_alpaca.return_value = None
    mock_yfinance.return_value = pd.DataFrame({'open': [100]})

    # Act
    data = pipeline.fetch_ohlcv_with_fallback("TEST", "2024-01-01", "2024-01-02")

    # Assert
    mock_alpaca.assert_called_once()
    mock_yfinance.assert_called_once()
    assert data is not None
    assert not data.empty

def test_data_partitioning(pipeline, tmp_path):
    """Test that data is saved in the correct partitioned structure."""
    # Arrange
    test_data = pd.DataFrame({
        'open': [100], 'high': [101], 'low': [99], 'close': [100.5], 'volume': [1000]
    }, index=pd.to_datetime(['2024-03-05 10:00:00']))
    
    # Act
    pipeline.save_data_partitioned(test_data, "TEST")

    # Assert
    expected_path = tmp_path / "data" / "raw" / "TEST" / "2024" / "03" / "05" / "TEST_20240305.parquet"
    expected_meta_path = expected_path.with_suffix('.json')
    
    assert expected_path.exists()
    assert expected_meta_path.exists()

@patch('data.pipeline.DataPipeline.save_data_partitioned')
def test_validation_integration(mock_save, pipeline):
    """Test that the validator is called and logs issues."""
    # Arrange: Create data with a known issue (negative price)
    bad_data = pd.DataFrame({'open': [-100]}, index=pd.to_datetime(['2024-01-01']))
    
    with patch.object(pipeline, 'fetch_ohlcv_with_fallback', return_value=bad_data):
        with patch.object(pipeline.logger, 'warning') as mock_log:
            # Act
            pipeline.process_universe_batch(["BADTICKER"], "2024-01-01", "2024-01-02")
            
            # Assert
            assert mock_log.called
            # Check that the log message contains details about the validation failure
            assert "Validation issues for BADTICKER" in mock_log.call_args[0][0]
            assert "price_outliers" in mock_log.call_args[0][0]
