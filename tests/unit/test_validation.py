"""
Unit Tests for DataValidator
"""
import pytest
import pandas as pd
from pathlib import Path
import sys

# Add src to path
sys.path.append(str(Path(__file__).parent.parent.parent / "src"))

from data.validation import DataValidator

@pytest.fixture
def validator():
    return DataValidator()

@pytest.fixture
def sample_good_data():
    """A sample of good OHLCV data."""
    return pd.DataFrame({
        'open': [100, 101, 102], 'high': [102, 102, 103],
        'low': [99, 100, 101], 'close': [101, 101.5, 102.5],
        'volume': [1000, 1100, 1200]
    }, index=pd.to_datetime(['2024-01-01 09:30:00', '2024-01-01 09:35:00', '2024-01-01 09:40:00']))

def test_good_data_passes(validator, sample_good_data):
    """Test that good data passes all validation checks."""
    result = validator.validate_ohlcv_data(sample_good_data, "GOOD")
    assert result["checks_failed"] == 0
    assert result["checks_passed"] == 4

def test_missing_values(validator, sample_good_data):
    """Test detection of missing values."""
    sample_good_data.loc[sample_good_data.index[1], 'close'] = None
    result = validator.validate_ohlcv_data(sample_good_data, "BAD")
    assert result["checks_failed"] == 1
    assert result["details"]["missing_values"]["valid"] is False
    assert "NaN values found" in result["details"]["missing_values"]["detail"]

def test_price_outliers(validator, sample_good_data):
    """Test detection of zero or negative prices."""
    sample_good_data.loc[sample_good_data.index[1], 'low'] = -1
    result = validator.validate_ohlcv_data(sample_good_data, "BAD")
    assert result["checks_failed"] == 1
    assert result["details"]["price_outliers"]["valid"] is False
    assert "zero or negative" in result["details"]["price_outliers"]["detail"]

def test_volume_outliers(validator, sample_good_data):
    """Test detection of negative volume."""
    sample_good_data.loc[sample_good_data.index[1], 'volume'] = -100
    result = validator.validate_ohlcv_data(sample_good_data, "BAD")
    assert result["checks_failed"] == 1
    assert result["details"]["volume_outliers"]["valid"] is False
    assert "negative values" in result["details"]["volume_outliers"]["detail"]

def test_data_gaps(validator, sample_good_data):
    """Test detection of time series gaps."""
    bad_data = sample_good_data.drop(sample_good_data.index[1])
    result = validator.validate_ohlcv_data(bad_data, "BAD")
    assert result["checks_failed"] == 1
    assert result["details"]["data_gaps"]["valid"] is False
    assert "unexpected gap(s)" in result["details"]["data_gaps"]["detail"]

def test_no_gaps_for_overnight(validator):
    """Test that overnight gaps are ignored."""
    data = pd.DataFrame({
        'open': [100, 101], 'high': [102, 102],
        'low': [99, 100], 'close': [101, 101.5],
        'volume': [1000, 1100]
    }, index=pd.to_datetime(['2024-01-01 15:55:00', '2024-01-02 09:30:00']))
    result = validator.validate_ohlcv_data(data, "GOOD")
    assert result["details"]["data_gaps"]["valid"] is True
