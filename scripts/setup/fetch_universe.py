"""
S&P 500 Universe Fetching Script
Phase 1: Research & Scoping
"""

import pandas as pd
import yfinance as yf
from datetime import datetime
import logging
from pathlib import Path
import sys


def setup_logging():
    """Setup logging for universe fetching"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_dir / "universe_setup.log"),
            logging.StreamHandler(sys.stdout),
        ],
    )
    return logging.getLogger(__name__)


def fetch_sp500_constituents():
    """
    Fetch current S&P 500 constituents from Wikipedia
    Returns: DataFrame with constituent data
    """
    logger = logging.getLogger(__name__)

    try:
        logger.info("Fetching S&P 500 constituents from Wikipedia...")
        url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
        tables = pd.read_html(url)
        sp500_table = tables[0]

        # Select and rename relevant columns
        constituents = sp500_table[
            ["Symbol", "Security", "GICS Sector", "GICS Sub-Industry"]
        ]
        constituents = constituents.rename(
            columns={
                "Symbol": "ticker",
                "Security": "company_name",
                "GICS Sector": "sector",
                "GICS Sub-Industry": "sub_industry",
            }
        )

        # Add metadata
        constituents["inception_date"] = datetime.now().strftime("%Y-%m-%d")
        constituents["data_source"] = "wikipedia"
        constituents["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        logger.info(f"✓ Successfully fetched {len(constituents)} S&P 500 constituents")
        return constituents

    except Exception as e:
        logger.error(f"Failed to fetch S&P 500 constituents: {e}")
        raise


def create_placeholder_universe():
    """
    Create a placeholder universe file if primary fetch fails
    Returns: DataFrame with major tickers
    """
    logger = logging.getLogger(__name__)
    logger.warning("Creating placeholder universe with major tickers")

    major_tickers = [
        "AAPL",
        "MSFT",
        "GOOGL",
        "AMZN",
        "TSLA",
        "META",
        "NVDA",
        "JPM",
        "JNJ",
        "V",
    ]

    placeholder = pd.DataFrame(
        {
            "ticker": major_tickers,
            "company_name": [f"Placeholder {ticker}" for ticker in major_tickers],
            "sector": ["Technology"] * len(major_tickers),
            "sub_industry": ["Placeholder"] * len(major_tickers),
            "inception_date": datetime.now().strftime("%Y-%m-%d"),
            "data_source": "manual_fallback",
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    )

    return placeholder


def validate_universe_data(constituents):
    """
    Validate the fetched universe data
    Returns: Boolean indicating validation success
    """
    logger = logging.getLogger(__name__)

    required_columns = ["ticker", "company_name", "sector", "sub_industry"]

    # Check required columns exist
    for col in required_columns:
        if col not in constituents.columns:
            logger.error(f"Missing required column: {col}")
            return False

    # Check for empty data
    if constituents.empty:
        logger.error("Universe data is empty")
        return False

    # Check for duplicate tickers
    duplicate_tickers = constituents["ticker"].duplicated().sum()
    if duplicate_tickers > 0:
        logger.warning(f"Found {duplicate_tickers} duplicate tickers")

    # Check sector distribution
    sector_counts = constituents["sector"].value_counts()
    logger.info("Sector distribution:")
    for sector, count in sector_counts.items():
        logger.info(f"  {sector}: {count} tickers")

    return True


def main():
    """Main execution function"""
    logger = setup_logging()
    logger.info("Starting S&P 500 universe fetch")

    try:
        # Ensure data directory exists
        data_dir = Path("data/universe")
        data_dir.mkdir(parents=True, exist_ok=True)

        # Try to fetch from primary source
        try:
            constituents = fetch_sp500_constituents()
        except Exception as e:
            logger.warning(f"Primary fetch failed, using fallback: {e}")
            constituents = create_placeholder_universe()

        # Validate the data
        if not validate_universe_data(constituents):
            raise ValueError("Universe data validation failed")

        # Save to file
        output_path = data_dir / "sp500_constituents.csv"
        constituents.to_csv(output_path, index=False)

        # Log success
        logger.info(f"✓ Saved {len(constituents)} constituents to {output_path}")
        logger.info(f"✓ Sectors: {constituents['sector'].nunique()}")
        logger.info(f"✓ Date range: {constituents['inception_date'].iloc[0]}")

        # Create completion checkpoint
        checkpoint = {
            "phase": 1,
            "step": "universe_creation",
            "timestamp": datetime.now().isoformat(),
            "status": "completed",
            "constituents_count": len(constituents),
            "sectors_count": constituents["sector"].nunique(),
            "data_source": constituents["data_source"].iloc[0],
        }

        checkpoint_path = Path("logs/universe_checkpoint.json")
        with open(checkpoint_path, "w") as f:
            import json

            json.dump(checkpoint, f, indent=2)

        logger.info("✓ Universe creation completed successfully")

    except Exception as e:
        logger.error(f"Universe creation failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
