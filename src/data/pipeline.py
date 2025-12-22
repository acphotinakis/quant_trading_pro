"""
Quant Trading Pro - Data Acquisition Pipeline
Phase 2: Data Acquisition & Infrastructure
"""

import pandas as pd
import numpy as np
import yaml
import logging
from pathlib import Path
from datetime import datetime, timedelta
import time
import requests
import sys
from typing import Dict, List, Optional
import hashlib
import json
import os
from alpaca_trade_api.rest import REST, TimeFrame
from .validation import DataValidator


class DataPipeline:
    def __init__(self, config_path: str = "config/data_sources.yaml"):
        self.logger = self._setup_logging()
        self.config = self._load_config(config_path)
        self.base_path = Path("data")
        self.staging_path = Path("staging/temp")
        self.cache_path = Path("staging/cache")
        self.staging_path.mkdir(parents=True, exist_ok=True)
        self.cache_path.mkdir(parents=True, exist_ok=True)
        self.validator = DataValidator()

        # Initialize providers
        self.providers = self._initialize_providers()

    def _setup_logging(self) -> logging.Logger:
        """Setup logging for data pipeline"""
        log_dir = Path("logs/data_pipeline")
        log_dir.mkdir(parents=True, exist_ok=True)

        logger = logging.getLogger("data_pipeline")
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            # File handler
            log_file = log_dir / f"daily_{datetime.now().strftime('%Y%m%d')}.log"
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.INFO)

            # Console handler
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.INFO)

            # Formatter
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)

            logger.addHandler(file_handler)
            logger.addHandler(console_handler)

        return logger

    def _load_config(self, config_path: str) -> Dict:
        """Load data sources configuration"""
        with open(config_path, "r") as f:
            return yaml.safe_load(f)

    def _initialize_providers(self) -> Dict:
        """Initialize data provider connectors"""
        providers = {}

        # Yahoo Finance provider (always available as fallback)
        try:
            import yfinance as yf

            providers["yfinance"] = {
                "module": yf,
                "rate_limit": self.config["providers"]["yfinance"]["rate_limit"],
                "last_call": datetime.now() - timedelta(minutes=1),
            }
            self.logger.info("✓ Yahoo Finance provider initialized")
        except ImportError:
            self.logger.warning("Yahoo Finance not available")

        # Alpaca provider (primary)
        try:
            import alpaca_trade_api as tradeapi

            api_key = os.getenv("APCA_API_KEY_ID")
            secret_key = os.getenv("APCA_API_SECRET_KEY")
            if not api_key or not secret_key:
                raise ValueError("Alpaca API keys not found in environment variables.")

            providers["alpaca"] = {
                "module": tradeapi,
                "api": REST(api_key, secret_key, base_url=self.config["providers"]["alpaca"]["data_url"]),
                "rate_limit": self.config["providers"]["alpaca"]["rate_limit"],
                "last_call": datetime.now() - timedelta(minutes=1),
            }
            self.logger.info("✓ Alpaca provider initialized")
        except (ImportError, ValueError) as e:
            self.logger.warning(f"Alpaca Trade API not available: {e}")

        return providers

    def _rate_limit(self, provider: str) -> None:
        """Implement rate limiting for API calls"""
        if provider in self.providers:
            provider_info = self.providers[provider]
            rate_limit = provider_info["rate_limit"]
            time_since_last = (
                datetime.now() - provider_info["last_call"]
            ).total_seconds()

            min_interval = 60.0 / rate_limit  # Convert to seconds between calls
            if time_since_last < min_interval:
                sleep_time = min_interval - time_since_last
                time.sleep(sleep_time)

            provider_info["last_call"] = datetime.now()

    def fetch_ohlcv_yfinance(
        self, ticker: str, start_date: str, end_date: str, interval: str = "5m"
    ) -> Optional[pd.DataFrame]:
        """Fetch OHLCV data from Yahoo Finance"""
        try:
            self._rate_limit("yfinance")
            self.logger.debug(f"Fetching {ticker} from Yahoo Finance")

            data = self.providers["yfinance"]["module"].download(
                ticker,
                start=start_date,
                end=end_date,
                interval=interval,
                progress=False,
                auto_adjust=False, # Keep raw data for now
            )

            if data is None or data.empty:
                return None

            data = data.rename(
                columns={
                    "Open": "open", "High": "high", "Low": "low",
                    "Close": "close", "Volume": "volume"
                }
            )
            return data[~data.index.duplicated(keep='first')]

        except Exception as e:
            self.logger.error(f"Yahoo Finance fetch failed for {ticker}: {e}")
            return None

    def fetch_ohlcv_alpaca(
        self, ticker: str, start_date: str, end_date: str, timeframe: str = "5Min"
    ) -> Optional[pd.DataFrame]:
        """Fetch OHLCV data from Alpaca with retry logic."""
        if "alpaca" not in self.providers:
            return None

        api = self.providers["alpaca"]["api"]
        max_retries = self.config["providers"]["alpaca"]["max_retries"]
        
        for attempt in range(max_retries):
            try:
                self._rate_limit("alpaca")
                self.logger.debug(f"Fetching {ticker} from Alpaca (Attempt {attempt + 1})")
                
                # Convert timeframe for Alpaca SDK
                tf = TimeFrame.Minute if timeframe == "1Min" else TimeFrame.Day if timeframe == "1Day" else TimeFrame.Minute * 5

                bars = api.get_bars(ticker, tf, start=start_date, end=end_date, adjustment='raw').df
                
                if bars.empty:
                    return None
                
                # Alpaca returns timezone-aware timestamps, which is good.
                return bars[~bars.index.duplicated(keep='first')]

            except Exception as e:
                self.logger.warning(f"Alpaca fetch failed for {ticker} on attempt {attempt + 1}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt) # Exponential backoff
                else:
                    self.logger.error(f"Alpaca fetch failed for {ticker} after {max_retries} attempts.")
                    return None
        return None

    def fetch_ohlcv_alpha_vantage(self, ticker: str, start_date: str, end_date: str) -> Optional[pd.DataFrame]:
        """Placeholder for Alpha Vantage integration."""
        self.logger.debug(f"Alpha Vantage provider not yet implemented for {ticker}.")
        return None

    def fetch_ohlcv_interactive_brokers(self, ticker: str, start_date: str, end_date: str) -> Optional[pd.DataFrame]:
        """Placeholder for Interactive Brokers integration."""
        self.logger.debug(f"Interactive Brokers provider not yet implemented for {ticker}.")
        return None

    def fetch_ohlcv_with_fallback(
        self, ticker: str, start_date: str, end_date: str
    ) -> Optional[pd.DataFrame]:
        """Fetch OHLCV data with provider fallback chain and caching."""
        
        # --- Caching Logic ---
        cache_key = f"{ticker}_{start_date}_{end_date}.parquet"
        cache_file = self.cache_path / cache_key
        if cache_file.exists():
            # Check if cache is recent (e.g., within 24 hours)
            if (datetime.now().timestamp() - cache_file.stat().st_mtime) < 86400:
                self.logger.info(f"✓ {ticker} loaded from cache")
                return pd.read_parquet(cache_file)

        providers = self.config["providers"]["fallback_chain"]
        data = None
        for provider in providers:
            if provider == "alpaca":
                data = self.fetch_ohlcv_alpaca(ticker, start_date, end_date)
            elif provider == "yfinance":
                data = self.fetch_ohlcv_yfinance(ticker, start_date, end_date)
            elif provider == "alpha_vantage":
                data = self.fetch_ohlcv_alpha_vantage(ticker, start_date, end_date)
            elif provider == "interactive_brokers":
                data = self.fetch_ohlcv_interactive_brokers(ticker, start_date, end_date)
            
            if data is not None and not data.empty:
                self.logger.info(f"✓ {ticker} fetched from {provider}")
                data.to_parquet(cache_file, compression="zstd") # Save to cache
                return data

        self.logger.error(f"All providers failed for {ticker}")
        return None

    def save_data_partitioned(self, data: pd.DataFrame, ticker: str) -> str:
        """Save data with ticker/year/month/day partitioning."""
        if data is None or data.empty:
            return None

        # Ensure data is sorted by time
        data = data.sort_index()

        # Group by date to handle multi-day fetches
        for date, group in data.groupby(data.index.date):
            partition_path = (
                self.base_path / "raw" / ticker /
                str(date.year) / f"{date.month:02d}" / f"{date.day:02d}"
            )
            partition_path.mkdir(parents=True, exist_ok=True)

            file_path = partition_path / f"{ticker}_{date.strftime('%Y%m%d')}.parquet"
            group.to_parquet(file_path, compression="zstd", engine="pyarrow")

            checksum = hashlib.md5(pd.util.hash_pandas_object(group).values).hexdigest()
            metadata = {
                "ticker": ticker, "data_points": len(group),
                "date_range": {"start": group.index.min().isoformat(), "end": group.index.max().isoformat()},
                "checksum": checksum, "saved_at": datetime.now().isoformat(),
                "file_size": file_path.stat().st_size,
            }
            metadata_path = file_path.with_suffix(".json")
            with open(metadata_path, "w") as f:
                json.dump(metadata, f, indent=2)
        
        self.logger.info(f"✓ Saved {len(data)} data points for {ticker} across {len(data.index.date.unique())} days.")
        return str(self.base_path / "raw" / ticker)


    def process_universe_batch(self, tickers: List[str], start_date: str, end_date: str, batch_size: int = 10) -> Dict:
        """Process a batch of tickers with parallelization and validation."""
        import concurrent.futures
        from tqdm import tqdm

        results = {}
        self.logger.info(f"Processing {len(tickers)} tickers from {start_date} to {end_date}")

        with concurrent.futures.ThreadPoolExecutor(max_workers=batch_size) as executor:
            future_to_ticker = {
                executor.submit(self.fetch_ohlcv_with_fallback, ticker, start_date, end_date): ticker
                for ticker in tickers
            }
            for future in tqdm(concurrent.futures.as_completed(future_to_ticker), total=len(tickers), desc="Downloading OHLCV"):
                ticker = future_to_ticker[future]
                validation_report = {}
                try:
                    data = future.result()
                    if data is not None:
                        validation_report = self.validator.validate_ohlcv_data(data, ticker)
                        if validation_report["checks_failed"] > 0:
                            self.logger.warning(f"Validation issues for {ticker}: {validation_report['details']}")
                        
                        file_path = self.save_data_partitioned(data, ticker)
                        if file_path:
                            results[ticker] = {"status": "Success", "validation": validation_report}
                    else:
                        results[ticker] = {"status": "Failed", "validation": "No data fetched."}

                except Exception as e:
                    self.logger.error(f"Batch processing failed for {ticker}: {e}")
                    results[ticker] = {"status": "Failed", "validation": str(e)}
        
        successful = sum(1 for res in results.values() if res["status"] == "Success")
        self.logger.info(f"Batch complete: {successful} successful, {len(tickers) - successful} failed")
        return results

    def select_top_k_universe(self, k: int = 50) -> pd.DataFrame:
        """Select top K stocks based on average daily dollar volume over the last 90 days."""
        self.logger.info(f"Selecting top {k} stocks for ML subset based on dollar volume.")
        
        universe_path = self.base_path / "universe" / "sp500_constituents.csv"
        if not universe_path.exists():
            self.logger.error(f"Universe file not found at {universe_path}. Run `fetch_universe.py` first.")
            return pd.DataFrame()
            
        universe = pd.read_csv(universe_path)
        tickers = universe["ticker"].tolist()

        end_date = datetime.now()
        start_date = end_date - timedelta(days=90)
        
        self.logger.info(f"Fetching daily data for {len(tickers)} tickers to calculate dollar volume...")
        
        # Use yfinance for daily data as it's generally reliable for this purpose
        daily_data = self.providers["yfinance"]["module"].download(
            tickers,
            start=start_date.strftime('%Y-%m-%d'),
            end=end_date.strftime('%Y-%m-%d'),
            interval="1d",
            progress=False,
            group_by='ticker'
        )
        
        dollar_volumes = {}
        for ticker in tickers:
            try:
                ticker_data = daily_data[ticker] if len(tickers) > 1 else daily_data
                if not ticker_data.empty:
                    avg_dollar_volume = (ticker_data['Close'] * ticker_data['Volume']).mean()
                    if pd.notna(avg_dollar_volume):
                        dollar_volumes[ticker] = avg_dollar_volume
            except KeyError:
                self.logger.warning(f"No daily data found for {ticker} to calculate dollar volume.")

        if not dollar_volumes:
            self.logger.error("Could not calculate dollar volumes. Falling back to simple selection.")
            return universe.head(k).copy()

        sorted_tickers = sorted(dollar_volumes.items(), key=lambda item: item[1], reverse=True)
        top_k_tickers = [ticker for ticker, volume in sorted_tickers[:k]]
        
        top_k_df = universe[universe['ticker'].isin(top_k_tickers)].copy()
        
        output_path = self.base_path / "processed" / f"topK_{k}.csv"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        top_k_df.to_csv(output_path, index=False)

        self.logger.info(f"✓ Top {k} universe based on dollar volume saved to {output_path}")
        return top_k_df

    def run_phase2_pipeline(self) -> bool:
        """Execute complete Phase 2 data pipeline."""
        try:
            self.logger.info("--- Starting Phase 2 Data Acquisition Pipeline ---")

            top_k_tickers_df = self.select_top_k_universe(50)
            if top_k_tickers_df.empty:
                self.logger.error("Could not select top K universe. Aborting pipeline.")
                return False
            
            top_k_list = top_k_tickers_df["ticker"].tolist()

            end_date = datetime.now().strftime("%Y-%m-%d")
            start_date = (datetime.now() - timedelta(days=5 * 365)).strftime("%Y-%m-%d")

            results = self.process_universe_batch(top_k_list, start_date, end_date, batch_size=10)

            self._generate_quality_report(results)

            checkpoint = {
                "phase": 2, "step": "data_acquisition", "timestamp": datetime.now().isoformat(),
                "status": "completed", "tickers_processed": len(results),
                "successful_downloads": sum(1 for r in results.values() if r["status"] == "Success"),
            }
            checkpoint_path = Path("logs/phase2_checkpoint.json")
            with open(checkpoint_path, "w") as f:
                json.dump(checkpoint, f, indent=2)

            self.logger.info("✓ Phase 2 data acquisition completed successfully")
            return True

        except Exception as e:
            self.logger.error(f"Phase 2 pipeline failed: {e}", exc_info=True)
            return False

    def _generate_quality_report(self, results: Dict) -> None:
        """Generate a dynamic data quality dashboard."""
        successful_downloads = sum(1 for r in results.values() if r["status"] == "Success")
        total_processed = len(results)
        success_rate = (successful_downloads / total_processed * 100) if total_processed > 0 else 0

        validation_rows = []
        for ticker, result in results.items():
            if result['status'] == 'Success':
                report = result['validation']
                failed_checks = [f"{k}: {v['detail']}" for k, v in report['details'].items() if not v['valid']]
                status_color = "orange" if failed_checks else "green"
                status_text = "Warning" if failed_checks else "OK"
                details = "<br>".join(failed_checks) if failed_checks else "All checks passed."
                validation_rows.append(f"""
                <tr>
                    <td>{ticker}</td>
                    <td style='color:{status_color};'>{status_text}</td>
                    <td>{report['checks_passed']} / {report['checks_passed'] + report['checks_failed']}</td>
                    <td>{details}</td>
                </tr>
                """)
            else:
                validation_rows.append(f"""
                <tr>
                    <td>{ticker}</td>
                    <td style='color:red;'>Failed</td>
                    <td>N/A</td>
                    <td>{result['validation']}</td>
                </tr>
                """)
        
        validation_table = "<table><tr><th>Ticker</th><th>Status</th><th>Checks Passed</th><th>Details</th></tr>" + "".join(validation_rows) + "</table>"

        report_content = f"""
        <html><head><title>Data Quality Dashboard - Phase 2</title>
        <style>
            body {{ font-family: sans-serif; }} table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #dddddd; text-align: left; padding: 8px; }}
            tr:nth-child(even) {{ background-color: #f2f2f2; }}
        </style>
        </head><body>
            <h1>Data Quality Dashboard - Phase 2</h1>
            <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <h3>Download Summary</h3>
            <p>Tickers Processed: {total_processed}</p>
            <p>Successful Downloads: {successful_downloads}</p>
            <p>Success Rate: {success_rate:.1f}%</p>
            <h3>Validation Details</h3>
            {validation_table}
        </body></html>
        """
        report_path = Path("reports/data_quality_dashboard.html")
        report_path.parent.mkdir(parents=True, exist_ok=True)
        with open(report_path, "w") as f:
            f.write(report_content)
        self.logger.info(f"✓ Data quality report saved to {report_path}")


def main():
    """Main execution function"""
    # For running this script, ensure you have a .env file with:
    # APCA_API_KEY_ID="YOUR_KEY"
    # APCA_API_SECRET_KEY="YOUR_SECRET"
    from dotenv import load_dotenv
    load_dotenv()
    
    pipeline = DataPipeline()
    success = pipeline.run_phase2_pipeline()

    if success:
        print("🎉 Phase 2 completed successfully!")
        sys.exit(0)
    else:
        print("💥 Phase 2 failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
