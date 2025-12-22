"""
Quant Trading Pro - EDA Pipeline
Phase 3: Exploratory Data Analysis
"""
import pandas as pd
import numpy as np
import yaml
import logging
from pathlib import Path
import sys
import concurrent.futures
from datetime import datetime, timedelta
from tqdm import tqdm
import warnings

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))
from features import analytics

# Suppress warnings from numpy polyfit
warnings.simplefilter('ignore', np.RankWarning)

def setup_logging() -> logging.Logger:
    """Setup logging for the EDA pipeline."""
    log_dir = Path("logs/eda")
    log_dir.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("eda_pipeline")
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        log_file = log_dir / f"eda_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.addHandler(logging.StreamHandler(sys.stdout))
        
    return logger

def load_ticker_data(ticker: str, data_path: Path, start_date: str, end_date: str) -> pd.DataFrame:
    """Loads all partitioned parquet files for a single ticker within a date range."""
    ticker_path = data_path / ticker
    if not ticker_path.is_dir():
        return pd.DataFrame()
    
    files = sorted(ticker_path.glob("**/*.parquet"))
    
    df_list = []
    for file in files:
        # Extract date from file path to filter
        try:
            file_date = pd.to_datetime(file.stem.split('_')[-1], format='%Y%m%d')
            if pd.to_datetime(start_date) <= file_date <= pd.to_datetime(end_date):
                df_list.append(pd.read_parquet(file))
        except (ValueError, IndexError):
            continue
            
    if not df_list:
        return pd.DataFrame()
        
    return pd.concat(df_list).sort_index()

def process_ticker(ticker: str, data_path: Path, start_date: str, end_date: str) -> pd.DataFrame:
    """Loads data and computes features for a single ticker."""
    logger = logging.getLogger("eda_pipeline")
    logger.info(f"Processing {ticker}...")
    
    try:
        intraday_df = load_ticker_data(ticker, data_path, start_date, end_date)
        if intraday_df.empty:
            logger.warning(f"No data found for {ticker} in the given date range.")
            return None
            
        daily_features = analytics.aggregate_to_daily_features(intraday_df)
        daily_features['ticker'] = ticker
        return daily_features
    except Exception as e:
        logger.error(f"Failed to process {ticker}: {e}", exc_info=True)
        return None

def main():
    """Main execution function for the EDA pipeline."""
    logger = setup_logging()
    logger.info("--- Starting Phase 3: Exploratory Data Analysis Pipeline ---")

    # Load config
    with open("config/eda.yaml", 'r') as f:
        config = yaml.safe_load(f)

    # Define paths and date ranges
    base_path = Path(".")
    data_path = base_path / "data" / "raw"
    output_path = base_path / "data" / "processed"
    plots_path = base_path / "plots"
    output_path.mkdir(exist_ok=True)
    plots_path.mkdir(exist_ok=True)
    
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=5 * 365)).strftime("%Y-%m-%d")

    # Load top-K universe
    try:
        top_k_df = pd.read_csv(output_path / "topK_50.csv")
        tickers = top_k_df['ticker'].tolist()
        logger.info(f"Loaded {len(tickers)} tickers from top-K universe.")
    except FileNotFoundError:
        logger.error("topK_50.csv not found. Please run Phase 2 pipeline first.")
        return

    # Process tickers in parallel
    all_features = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        future_to_ticker = {executor.submit(process_ticker, ticker, data_path, start_date, end_date): ticker for ticker in tickers}
        for future in tqdm(concurrent.futures.as_completed(future_to_ticker), total=len(tickers), desc="Computing Features"):
            result = future.result()
            if result is not None:
                all_features.append(result)

    if not all_features:
        logger.error("No features were generated. Aborting.")
        return

    # Combine and process final feature DataFrame
    logger.info("Combining and normalizing all features...")
    combined_df = pd.concat(all_features).set_index(['ticker', pd.Grouper(level=0, freq='D')])
    
    feature_cols = [col for col in combined_df.columns if col not in ['open', 'high', 'low', 'close', 'volume']]
    
    # Cross-sectional normalization
    norm_method = config['analysis_params']['normalization_method']
    if norm_method == 'rank':
        combined_df[feature_cols] = analytics.cross_sectional_normalize(combined_df, feature_cols)
    else:
        logger.warning(f"Normalization method '{norm_method}' not implemented. Skipping.")

    # Save final feature set
    final_feature_path = output_path / "eda_features.parquet"
    combined_df.to_parquet(final_feature_path)
    logger.info(f"✓ Final feature set saved to {final_feature_path}")

    # --- Feature Analysis ---
    logger.info("Performing feature analysis...")
    
    # Correlation Analysis
    correlation_matrix = combined_df[feature_cols].corr()
    correlation_path = output_path / "feature_correlations.csv"
    correlation_matrix.to_csv(correlation_path)
    logger.info(f"✓ Feature correlation matrix saved to {correlation_path}")

    # Distribution Analysis & Visualization (for a sample feature)
    try:
        import matplotlib.pyplot as plt
        import seaborn as sns

        sample_feature = 'dollar_volume'
        plt.figure(figsize=(10, 6))
        sns.histplot(combined_df[sample_feature], bins=50, kde=True)
        plt.title(f'Distribution of {sample_feature}')
        plt.xlabel(sample_feature)
        plt.ylabel('Frequency')
        plot_path = plots_path / f"{sample_feature}_distribution.png"
        plt.savefig(plot_path)
        plt.close()
        logger.info(f"✓ Sample distribution plot saved to {plot_path}")
    except ImportError:
        logger.warning("Matplotlib or Seaborn not installed. Skipping plot generation.")

    logger.info("--- Phase 3: EDA Pipeline Completed Successfully ---")

if __name__ == "__main__":
    import os
    main()
