"""
Quant Trading Pro - Feature Calculation Analytics
Phase 3: Exploratory Data Analysis
"""
import pandas as pd
import numpy as np
from numpy.polynomial.polynomial import polyfit
from typing import List

def calculate_dollar_volume(df: pd.DataFrame) -> pd.Series:
    """Calculates daily dollar volume."""
    return df['close'] * df['volume']

def calculate_amihud_illiquidity(df: pd.DataFrame) -> pd.Series:
    """Calculates daily Amihud Illiquidity metric."""
    log_returns = np.log(df['close']).diff()
    dollar_volume = df['close'] * df['volume']
    # Avoid division by zero
    dollar_volume[dollar_volume == 0] = np.nan
    return (log_returns.abs() / dollar_volume).dropna()

def calculate_realized_volatility(df: pd.DataFrame) -> pd.Series:
    """Calculates daily realized volatility from intraday log returns."""
    log_returns = np.log(df['close']).diff()
    return log_returns.std()

def calculate_skewness(df: pd.DataFrame) -> pd.Series:
    """Calculates daily skewness of intraday log returns."""
    log_returns = np.log(df['close']).diff()
    return log_returns.skew()

def calculate_kurtosis(df: pd.DataFrame) -> pd.Series:
    """Calculates daily kurtosis of intraday log returns."""
    log_returns = np.log(df['close']).diff()
    return log_returns.kurt()

def calculate_rolling_slope(series: pd.Series, window: int) -> pd.Series:
    """Calculates the slope of a rolling linear regression."""
    def get_slope(data):
        y = data.values
        x = np.arange(len(y))
        b, m = polyfit(x, y, 1)
        return m
    return series.rolling(window=window).apply(get_slope, raw=False)

def calculate_hurst_exponent(series: pd.Series, max_lags: int = 100) -> float:
    """
    Calculates the Hurst Exponent of a time series using Rescaled Range (R/S) analysis.
    A simplified implementation.
    """
    if len(series) < max_lags:
        return np.nan
        
    lags = range(2, max_lags)
    tau = [np.sqrt(np.std(np.subtract(series[lag:], series[:-lag]))) for lag in lags]
    poly = polyfit(np.log(lags), np.log(tau), 1)
    return poly[1]

def aggregate_to_daily_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregates 5-minute intraday data to compute daily features.
    """
    if df.empty:
        return pd.DataFrame()

    # Resample to daily frequency
    daily_df = df.resample('D').agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum'
    }).dropna()

    if daily_df.empty:
        return pd.DataFrame()

    # --- Liquidity ---
    daily_df['dollar_volume'] = calculate_dollar_volume(daily_df)
    daily_df['amihud_illiquidity'] = calculate_amihud_illiquidity(daily_df)
    
    # --- Volatility (from intraday) ---
    intraday_vol = df.groupby(df.index.date).apply(calculate_realized_volatility)
    intraday_skew = df.groupby(df.index.date).apply(calculate_skewness)
    intraday_kurt = df.groupby(df.index.date).apply(calculate_kurtosis)
    
    daily_df['realized_volatility'] = intraday_vol
    daily_df['skewness'] = intraday_skew
    daily_df['kurtosis'] = intraday_kurt

    # --- Trendiness ---
    daily_df['slope_21d'] = calculate_rolling_slope(daily_df['close'], window=21)
    
    # Hurst exponent is a single value for the series, can be calculated on daily closes
    hurst_val = calculate_hurst_exponent(daily_df['close'])
    daily_df['hurst'] = hurst_val # Broadcast single value to all rows

    return daily_df.dropna()

def cross_sectional_normalize(df: pd.DataFrame, feature_cols: List[str]) -> pd.DataFrame:
    """
    Performs cross-sectional ranking normalization.
    Converts feature values to ranks (0 to 1) for each day.
    """
    return df.groupby(level='date')[feature_cols].transform(
        lambda x: x.rank(method='first', pct=True)
    )
