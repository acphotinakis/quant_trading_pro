"""
Unit Tests for Feature Analytics
Phase 3: Exploratory Data Analysis
"""
import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add src to path
sys.path.append(str(Path(__file__).parent.parent.parent / "src"))
from features import analytics

@pytest.fixture
def sample_intraday_data():
    """Create a sample intraday DataFrame."""
    dates = pd.to_datetime(['2024-01-01 09:30', '2024-01-01 09:35', '2024-01-01 09:40',
                            '2024-01-02 09:30', '2024-01-02 09:35', '2024-01-02 09:40'])
    data = {
        'open': [100, 101, 100.5, 102, 103, 102.5],
        'high': [101.5, 101.5, 101, 103.5, 103.5, 103],
        'low': [99.5, 100.5, 100, 101.5, 102.5, 102],
        'close': [101, 100.5, 100.8, 103, 102.5, 102.8],
        'volume': [1000, 1200, 1100, 1500, 1400, 1600]
    }
    return pd.DataFrame(data, index=dates)

def test_calculate_dollar_volume(sample_intraday_data):
    daily_data = sample_intraday_data.resample('D').agg({'close': 'last', 'volume': 'sum'})
    dollar_volume = analytics.calculate_dollar_volume(daily_data)
    assert isinstance(dollar_volume, pd.Series)
    assert not dollar_volume.isnull().any()
    assert dollar_volume.iloc[0] == 100.8 * (1000 + 1200 + 1100)

def test_calculate_realized_volatility(sample_intraday_data):
    volatility = analytics.calculate_realized_volatility(sample_intraday_data)
    assert isinstance(volatility, float)
    assert volatility > 0

def test_calculate_rolling_slope():
    series = pd.Series(np.arange(10))
    slope = analytics.calculate_rolling_slope(series, window=5)
    assert isinstance(slope, pd.Series)
    # The slope of y=x is 1
    assert np.isclose(slope.iloc[-1], 1.0)

def test_aggregate_to_daily_features(sample_intraday_data):
    daily_features = analytics.aggregate_to_daily_features(sample_intraday_data)
    assert isinstance(daily_features, pd.DataFrame)
    assert len(daily_features) == 2 # Two days of data
    assert 'dollar_volume' in daily_features.columns
    assert 'realized_volatility' in daily_features.columns
    assert 'slope_21d' in daily_features.columns
    assert not daily_features.isnull().values.any()

def test_cross_sectional_normalize(sample_intraday_data):
    # Create a multi-index dataframe similar to the pipeline output
    df1 = analytics.aggregate_to_daily_features(sample_intraday_data)
    df1['ticker'] = 'AAPL'
    df2 = df1.copy()
    df2['ticker'] = 'GOOG'
    df2['dollar_volume'] *= 2 # Make GOOG have higher dollar volume
    
    combined = pd.concat([df1, df2]).set_index(['ticker', pd.Grouper(level=0, freq='D')])
    feature_cols = ['dollar_volume', 'realized_volatility']
    
    normalized_df = analytics.cross_sectional_normalize(combined, feature_cols)
    
    # For each day, AAPL should have rank 0.5 and GOOG should have rank 1.0 for dollar_volume
    assert normalized_df.loc[('AAPL', pd.to_datetime('2024-01-01'))]['dollar_volume'] == 0.5
    assert normalized_df.loc[('GOOG', pd.to_datetime('2024-01-01'))]['dollar_volume'] == 1.0
