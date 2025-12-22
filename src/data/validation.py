"""
Quant Trading Pro - Data Validation Module
Phase 2: Data Acquisition & Infrastructure
"""
import pandas as pd
from typing import Dict, List

class DataValidator:
    """
    A class to perform validation checks on OHLCV data.
    """

    def validate_ohlcv_data(self, data: pd.DataFrame, ticker: str) -> Dict:
        """
        Runs a suite of validation checks on the given OHLCV DataFrame.

        Args:
            data (pd.DataFrame): The OHLCV data to validate.
            ticker (str): The ticker symbol for the data.

        Returns:
            Dict: A dictionary containing the results of the validation checks.
        """
        if data is None or data.empty:
            return {"ticker": ticker, "error": "Data is empty or None."}

        results = {
            "ticker": ticker,
            "checks_passed": 0,
            "checks_failed": 0,
            "details": {},
        }

        checks = {
            "missing_values": self._check_missing_values,
            "price_outliers": self._check_price_outliers,
            "volume_outliers": self._check_volume_outliers,
            "data_gaps": self._check_data_gaps,
        }

        for check_name, check_func in checks.items():
            is_valid, detail = check_func(data)
            if is_valid:
                results["checks_passed"] += 1
            else:
                results["checks_failed"] += 1
            results["details"][check_name] = {"valid": is_valid, "detail": detail}
        
        return results

    def _check_missing_values(self, data: pd.DataFrame) -> (bool, str):
        """Check for any missing values in key columns."""
        required_cols = ['open', 'high', 'low', 'close', 'volume']
        missing_cols = [col for col in required_cols if col not in data.columns]
        if missing_cols:
            return False, f"Missing columns: {', '.join(missing_cols)}"

        if data[required_cols].isnull().values.any():
            null_counts = data[required_cols].isnull().sum()
            details = ", ".join([f"{col}: {count}" for col, count in null_counts.items() if count > 0])
            return False, f"NaN values found. Counts: {details}"
        return True, "No missing values found."

    def _check_price_outliers(self, data: pd.DataFrame) -> (bool, str):
        """Check for basic price outliers (e.g., zero or negative prices)."""
        price_cols = ['open', 'high', 'low', 'close']
        if (data[price_cols] <= 0).values.any():
            return False, "Found zero or negative values in price columns."
        return True, "No zero or negative prices found."

    def _check_volume_outliers(self, data: pd.DataFrame) -> (bool, str):
        """Check for volume outliers (e.g., negative volume)."""
        if (data['volume'] < 0).values.any():
            return False, "Found negative values in volume column."
        return True, "No negative volumes found."

    def _check_data_gaps(self, data: pd.DataFrame) -> (bool, str):
        """Check for significant gaps in the time series index."""
        if not isinstance(data.index, pd.DatetimeIndex):
            return False, "Index is not a DatetimeIndex."
        
        # Assuming 5-minute interval for this check
        diffs = data.index.to_series().diff().dropna()
        
        # Check for gaps larger than the expected interval (e.g., > 5 mins during market hours)
        # This is a simplified check. A robust implementation would only check during market hours.
        frequent_diff = diffs.mode()[0]
        if frequent_diff > pd.Timedelta(minutes=5):
             return True, f"High frequency data detected with interval {frequent_diff}, skipping gap check."


        gaps = diffs[diffs > pd.Timedelta(minutes=5)]
        
        # Ignore overnight and weekend gaps
        overnight_gaps = gaps[gaps > pd.Timedelta(hours=1)]
        
        num_gaps = len(gaps) - len(overnight_gaps)
        
        if num_gaps > 0:
            return False, f"Found {num_gaps} unexpected gap(s) in the time series."
        return True, "No significant data gaps found."