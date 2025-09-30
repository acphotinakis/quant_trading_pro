"""
Data Validation Module
Phase 2: Data Acquisition & Infrastructure
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Tuple


class DataValidator:
    def __init__(self):
        self.logger = logging.getLogger("data_validation")
        self.base_path = Path("data")

    def validate_ohlcv_data(self, data: pd.DataFrame, ticker: str) -> Dict:
        """Validate OHLCV data quality"""
        validation_results = {
            "ticker": ticker,
            "timestamp": datetime.now().isoformat(),
            "checks_passed": 0,
            "checks_failed": 0,
            "issues": [],
        }

        if data is None or data.empty:
            validation_results["issues"].append("Data is empty or None")
            validation_results["checks_failed"] += 1
            return validation_results

        # Check 1: Required columns exist
        required_cols = ["open", "high", "low", "close", "volume"]
        missing_cols = [col for col in required_cols if col not in data.columns]
        if missing_cols:
            validation_results["issues"].append(f"Missing columns: {missing_cols}")
            validation_results["checks_failed"] += 1
        else:
            validation_results["checks_passed"] += 1

        # Check 2: No negative prices
        price_cols = ["open", "high", "low", "close"]
        negative_prices = data[price_cols].lt(0).any().any()
        if negative_prices:
            validation_results["issues"].append("Negative prices detected")
            validation_results["checks_failed"] += 1
        else:
            validation_results["checks_passed"] += 1

        # Check 3: High >= Low
        invalid_high_low = (data["high"] < data["low"]).any()
        if invalid_high_low:
            validation_results["issues"].append("High < Low detected")
            validation_results["checks_failed"] += 1
        else:
            validation_results["checks_passed"] += 1

        # Check 4: No duplicate timestamps
        duplicate_timestamps = data.index.duplicated().sum()
        if duplicate_timestamps > 0:
            validation_results["issues"].append(
                f"{duplicate_timestamps} duplicate timestamps"
            )
            validation_results["checks_failed"] += 1
        else:
            validation_results["checks_passed"] += 1

        # Check 5: Reasonable volume
        zero_volume = (data["volume"] == 0).sum()
        if zero_volume > len(data) * 0.1:  # More than 10% zero volume
            validation_results["issues"].append(
                f"High zero volume: {zero_volume} records"
            )
            validation_results["checks_failed"] += 1
        else:
            validation_results["checks_passed"] += 1

        # Check 6: Data completeness
        expected_days = (data.index.max() - data.index.min()).days
        actual_days = len(data)
        completeness = actual_days / expected_days if expected_days > 0 else 0

        if completeness < 0.95:
            validation_results["issues"].append(f"Low completeness: {completeness:.1%}")
            validation_results["checks_failed"] += 1
        else:
            validation_results["checks_passed"] += 1

        validation_results["completeness"] = completeness
        validation_results["total_checks"] = 6

        return validation_results

    def validate_macro_data(self, data: pd.DataFrame) -> Dict:
        """Validate macro indicator data"""
        validation_results = {
            "type": "macro_indicators",
            "timestamp": datetime.now().isoformat(),
            "checks_passed": 0,
            "checks_failed": 0,
            "issues": [],
        }

        required_indicators = ["VIX", "TNX_10Y", "IRX_3M", "YIELD_CURVE"]
        missing_indicators = [
            ind for ind in required_indicators if ind not in data.columns
        ]

        if missing_indicators:
            validation_results["issues"].append(
                f"Missing indicators: {missing_indicators}"
            )
            validation_results["checks_failed"] += 1
        else:
            validation_results["checks_passed"] += 1

        # Check for extreme values (anomaly detection)
        vix_anomalies = data["VIX"][data["VIX"] > 100]  # VIX > 100 is extreme
        if len(vix_anomalies) > 0:
            validation_results["issues"].append(
                f"VIX anomalies: {len(vix_anomalies)} records > 100"
            )
            validation_results["checks_failed"] += 1
        else:
            validation_results["checks_passed"] += 1

        return validation_results

    def generate_validation_report(self, validation_results: List[Dict]) -> str:
        """Generate comprehensive validation report"""
        total_checks = sum(
            [r["checks_passed"] + r["checks_failed"] for r in validation_results]
        )
        passed_checks = sum([r["checks_passed"] for r in validation_results])
        failed_checks = sum([r["checks_failed"] for r in validation_results])

        report = f"""
        DATA VALIDATION REPORT
        Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        SUMMARY:
        - Total Checks: {total_checks}
        - Passed: {passed_checks} ({passed_checks/total_checks*100:.1f}%)
        - Failed: {failed_checks} ({failed_checks/total_checks*100:.1f}%)
        
        DETAILED RESULTS:
        """

        for result in validation_results:
            report += (
                f"\n{result['ticker'] if 'ticker' in result else 'Macro Indicators'}:\n"
            )
            report += f"  Passed: {result['checks_passed']}/{result['total_checks']}\n"
            if result["issues"]:
                report += "  Issues:\n"
                for issue in result["issues"]:
                    report += f"    - {issue}\n"

        return report
