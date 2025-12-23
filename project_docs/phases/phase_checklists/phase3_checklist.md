# Quant Trading Pro - Phase 3 Checklist

This checklist outlines the necessary tasks to complete Phase 3: Exploratory Data Analysis (EDA). The goal is to compute, analyze, and validate a set of ML-ready features based on the data acquired in Phase 2.

---

### 1. Setup & Configuration

- [x] **Create EDA Pipeline Script:**
    - [x] Create the main pipeline script at `src/features/eda_pipeline.py`. This script will orchestrate the entire EDA process.
- [x] **Create Feature Calculation Module:**
    - [x] Create a module at `src/features/analytics.py` to house the functions that calculate the individual liquidity, volatility, and trendiness metrics.
- [x] **Create EDA Configuration File:**
    - [x] Create `config/eda.yaml` to store parameters for this phase, such as rolling window lengths, normalization methods, and stability thresholds.
- [x] **Create Test File:**
    - [x] Create `tests/unit/test_features.py` to house unit tests for the new feature calculation functions.

### 2. Data Loading and Preprocessing

- [x] **Implement Data Loader:**
    - [x] In `eda_pipeline.py`, create a function to read the partitioned Parquet data from the `data/raw/` directory for the tickers specified in `data/processed/topK_50.csv`.
    - [x] The loader must be able to handle loading data for a specified date range and for multiple tickers.
- [x] **Data Preprocessing:**
    - [x] Ensure 5-minute data is correctly aligned for each trading session (e.g., handle market open/close times).
    - [x] Verify that data adjustments for splits/dividends are handled or noted. *(Note: This was deferred in Phase 2, so the EDA should proceed with raw data but the limitation should be documented).*

### 3. Feature Computation

- [x] **Implement Liquidity Metrics:** In `src/features/analytics.py`, create functions to calculate:
    - [x] Dollar Volume (DV)
    - [x] Turnover Ratio (TO)
    - [x] Amihud Illiquidity (ILLIQ)
- [x] **Implement Volatility Metrics:** In `src/features/analytics.py`, create functions to calculate:
    - [x] Realized Volatility (e.g., standard deviation of 5-minute log returns).
    - [x] Skewness of intraday returns.
    - [x] Kurtosis of intraday returns.
    - [x] A function to aggregate these intraday metrics to a daily frequency.
- [x] **Implement Trendiness Metrics:** In `src/features/analytics.py`, create functions to calculate:
    - [x] Rolling regression slopes on price (configurable window).
    - [x] Hurst Exponent.
    - [x] Spectral Analysis (e.g., using FFT to find dominant cycle periods).

### 4. Feature Analysis and Validation

- [x] **Normalization:**
    - [x] Implement functions for cross-sectional normalization (e.g., ranking or z-scoring across all stocks at a point in time).
    - [x] Implement functions for rolling-window normalization (e.g., z-scoring over a lookback period for a single stock).
- [x] **Stability Analysis:**
    - [x] Compute rank correlations of features across different rolling windows (e.g., 30-day vs. 90-day) to measure feature stability.
    - [x] Generate and save a feature stability report.
- [x] **Correlation Analysis:**
    - [x] Generate and save a feature correlation matrix (`data/processed/feature_correlations.csv`) to identify and document multicollinearity.
- [x] **Distribution Analysis & Visualization:**
    - [x] Generate and save plots (histograms, box plots) to the `plots/` directory for the distribution of each key feature.
    - [x] Generate and save plots showing feature behavior over time and across different market regimes (if regime data is available).

### 5. Infrastructure & Pipeline

- [x] **Build out `eda_pipeline.py`:**
    - [x] The script should load the top-K universe.
    - [x] It must iterate through each ticker, load its data, compute all features, normalize them, and save the results.
    - [x] Implement batch or parallel processing (e.g., using `concurrent.futures` or `dask`) to efficiently process all tickers.
    - [x] Add robust logging to `logs/eda/` to track progress, errors, and feature generation statistics.

### 6. Deliverables & Documentation

- [x] **Final Feature Set:**
    - [x] Save the final, computed, and normalized feature set for all top-K stocks to `data/processed/eda_features.parquet`.
- [x] **Unit Tests:**
    - [x] Implement unit tests in `tests/unit/test_features.py` for each individual feature calculation function to ensure correctness.
- [x] **Documentation:**
    - [x] Create the handoff document `docs/phase3_to_phase4.md`, summarizing the generated features and outlining how they should be used in the next phase.
    - [x] Ensure all new functions and modules have clear, descriptive docstrings.
