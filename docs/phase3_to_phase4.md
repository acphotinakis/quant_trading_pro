# Handoff: Phase 3 (EDA) to Phase 4 (Modeling)

## 1. Phase 3 Summary

Phase 3 focused on Exploratory Data Analysis (EDA) and feature engineering. The primary goal was to transform the raw 5-minute price and volume data into a set of daily, ML-ready features that capture various aspects of stock behavior.

The `src/features/eda_pipeline.py` script was created to orchestrate this process. It loads the top-K universe, processes each stock in parallel, computes a suite of features, normalizes them, and saves the final dataset.

---

## 2. Key Deliverables

- **Final Feature Set (`data/processed/eda_features.parquet`):**
  - A Parquet file containing the daily feature set for all stocks in the `topK_50.csv` universe.
  - The data is indexed by `ticker` and `date`.
  - All features have been cross-sectionally rank-normalized (from 0 to 1) for each day, making them comparable across different stocks.

- **Feature Correlation Matrix (`data/processed/feature_correlations.csv`):**
  - A CSV file showing the correlation between all generated features. This should be reviewed during model development to manage multicollinearity (e.g., through feature selection or regularization).

- **Feature Calculation Module (`src/features/analytics.py`):**
  - Contains all the core logic for calculating individual features.

- **Unit Tests (`tests/unit/test_features.py`):**
  - Unit tests verifying the correctness of the feature calculation functions.

---

## 3. Generated Features

The following features were computed and are available in the final dataset.

### 3.1. Liquidity Features
- **`dollar_volume`**: `close * volume`. A measure of the total value traded.
- **`amihud_illiquidity`**: `abs(return) / dollar_volume`. A measure of price impact; higher values suggest lower liquidity.

### 3.2. Volatility Features
- **`realized_volatility`**: Standard deviation of 5-minute log returns. Captures intraday price fluctuation.
- **`skewness`**: Skewness of 5-minute log returns. Measures the asymmetry of the intraday return distribution.
- **`kurtosis`**: Kurtosis of 5-minute log returns. Measures the "tailedness" of the intraday return distribution.

### 3.3. Trendiness Features
- **`slope_21d`**: The slope of a 21-day rolling linear regression on the closing price. Captures the short-term price trend.
- **`hurst`**: The Hurst Exponent calculated on daily closing prices. A value > 0.5 suggests trending behavior, < 0.5 suggests mean-reverting behavior, and ~0.5 suggests a random walk.

---

## 4. Inputs for Phase 4 (Modeling)

- **Primary Input:** The `data/processed/eda_features.parquet` file is the primary input for the modeling phase.
- **Target Variable:** A target variable (e.g., forward returns) needs to be defined and engineered. This was not part of the EDA phase. The modeling phase should start by creating this `y` variable.
- **Feature Selection:** Review the `feature_correlations.csv` matrix. Highly correlated features (e.g., > 0.9) may need to be handled. Consider using techniques like PCA or selecting one feature from a correlated pair.
- **Model Training:** The normalized features can be used directly in tree-based models (like LightGBM or XGBoost). For linear models, further scaling (like standardization) might be beneficial, although ranking already helps put them on a similar scale.
- **Backtesting:** The output of the model (e.g., predicted returns or rankings) will be used in the backtesting phase to simulate trading strategies.
