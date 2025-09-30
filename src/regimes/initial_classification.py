"""
Initial Market Regime Classification
Phase 1: Research & Scoping
"""

import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import logging
from pathlib import Path
import json
import yaml


class InitialRegimeClassifier:
    def __init__(self, config_path="config/regime_definitions.yaml"):
        self.logger = logging.getLogger(__name__)
        self.config = self.load_config(config_path)
        self.data_dir = Path("data/regimes")
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def load_config(self, config_path):
        """Load regime classification configuration"""
        with open(config_path, "r") as f:
            return yaml.safe_load(f)

    def fetch_macro_data(self, start_date="2010-01-01"):
        """Fetch VIX, Treasury yields, and market breadth data"""
        self.logger.info("Fetching macro regime indicators...")

        end_date = datetime.now().strftime("%Y-%m-%d")

        try:
            # VIX data
            vix = yf.download("^VIX", start=start_date, end=end_date, progress=False)
            vix = vix["Close", "^VIX"].copy()
            vix.name = "VIX"

            tnx = yf.download("^TNX", start=start_date, end=end_date, progress=False)
            tnx = tnx["Close", "^TNX"].copy()
            tnx.name = "TNX_10Y"

            irx = yf.download("^IRX", start=start_date, end=end_date, progress=False)
            irx = irx["Close", "^IRX"].copy()
            irx.name = "IRX_3M"

            # Yield curve
            yield_curve = (tnx - irx).rename("YIELD_CURVE")

            # Combine all data
            macro_data = pd.concat([vix, tnx, irx, yield_curve], axis=1)
            macro_data = macro_data.dropna()

            self.logger.info(f"✓ Fetched {len(macro_data)} days of macro data")
            return macro_data

        except Exception as e:
            self.logger.error(f"Failed to fetch macro data: {e}")
            raise

    def classify_regimes(self, macro_data):
        """Classify market regimes based on macro indicators"""
        self.logger.info("Classifying market regimes...")

        regimes = pd.DataFrame(index=macro_data.index)

        # VIX-based regimes
        vix_thresholds = self.config["regime_indicators"]["vix"]["thresholds"]
        regimes["vix_regime"] = pd.cut(
            macro_data["VIX"],
            bins=[0, vix_thresholds["low_vol"], vix_thresholds["high_vol"], 100],
            labels=["low_vol", "medium_vol", "high_vol"],
        )

        # Yield curve regimes
        yield_thresholds = self.config["regime_indicators"]["treasury_yields"][
            "spread_thresholds"
        ]
        regimes["yield_regime"] = np.where(
            macro_data["YIELD_CURVE"] < yield_thresholds["inverted"],
            "inverted",
            "normal",
        )

        # Simple breadth proxy (using VIX as momentum indicator)
        vix_rolling = macro_data["VIX"].rolling(window=21)
        regimes["momentum"] = np.where(
            macro_data["VIX"] < vix_rolling.mean() - vix_rolling.std(),
            "bullish",
            np.where(
                macro_data["VIX"] > vix_rolling.mean() + vix_rolling.std(),
                "bearish",
                "neutral",
            ),
        )

        # Composite regime classification
        conditions = [
            (regimes["vix_regime"] == "low_vol") & (regimes["momentum"] == "bullish"),
            (regimes["vix_regime"] == "high_vol"),
            (regimes["yield_regime"] == "inverted"),
            (regimes["vix_regime"] == "low_vol")
            | (regimes["vix_regime"] == "medium_vol"),
        ]

        choices = [
            "low_vol_bullish",
            "high_vol_stress",
            "inverted_yield",
            "medium_vol_normal",
        ]
        regimes["composite_regime"] = np.select(
            conditions, choices, default="medium_vol_normal"
        )

        self.logger.info("✓ Regime classification completed")
        return regimes

    def calculate_regime_stats(self, regimes):
        """Calculate statistics for each regime"""
        regime_stats = regimes["composite_regime"].value_counts().to_dict()
        total_days = len(regimes)

        stats = {
            "total_days": total_days,
            "regime_distribution": {
                regime: {"count": count, "percentage": count / total_days}
                for regime, count in regime_stats.items()
            },
            "current_regime": (
                regimes["composite_regime"].iloc[-1] if len(regimes) > 0 else "unknown"
            ),
            "last_update": datetime.now().isoformat(),
        }

        return stats

    def run(self):
        """Execute complete regime classification pipeline"""
        try:
            # Fetch data
            macro_data = self.fetch_macro_data()

            # Classify regimes
            regimes = self.classify_regimes(macro_data)

            # Combine with macro data
            full_data = pd.concat([macro_data, regimes], axis=1)

            # Save results
            full_data.to_parquet(self.data_dir / "initial_regime_data.parquet")
            regimes.to_parquet(self.data_dir / "regime_classifications.parquet")

            # Calculate and save statistics
            stats = self.calculate_regime_stats(regimes)
            with open(self.data_dir / "regime_statistics.json", "w") as f:
                json.dump(stats, f, indent=2)

            self.logger.info("✓ Initial regime classification completed")
            return stats

        except Exception as e:
            self.logger.error(f"Regime classification failed: {e}")
            raise


def main():
    """Main execution function"""
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    classifier = InitialRegimeClassifier()
    stats = classifier.run()

    print("\nRegime Classification Results:")
    print(f"Current regime: {stats['current_regime']}")
    print("Distribution:")
    for regime, data in stats["regime_distribution"].items():
        print(f"  {regime}: {data['percentage']:.1%}")


if __name__ == "__main__":
    main()
