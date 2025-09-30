# **Quant Trading Pro – Refined Integration Plan**

## **Phase 1 – Research & Scoping**

**Objective:** Define project goals, universe, data sources, constraints, success metrics, and prepare project infrastructure.

**Key Deliverables:**

1. **Objectives & Scope**

   * `docs/project_objectives.md`: Plain-English statement.
   * Define horizon (3–10 days), relative ranking, absolute prediction.
   * Confirm initial US equities focus (S&P500, ETFs optional later).

2. **Universe Selection**

   * `data/universe/sp500_constituents.csv`
   * Notes: `docs/universe_notes.md` (current members only).

3. **Data Source Evaluation**

   * `docs/data_sources.md`: Provider comparison (coverage, reliability, limits).
   * Example OHLCV pulls and plots for data sanity checks.

4. **Constraints & Assumptions**

   * `config/system_limits.yaml`: storage, runtime, API call budget.
   * `docs/constraints.md`: impact on horizon and data resolution.

5. **Success Metrics & Risk**

   * `docs/strategy_success.md`: Sharpe, turnover-adjusted Sharpe, max drawdown.
   * `docs/risk_matrix.md`: mitigations for missing data, compute limits, overfitting.

6. **Project Management Setup**

   * Git repo with `/docs`, `/config`, `/data/universe`.
   * Timeline: `docs/project_timeline.md`.
   * Task management: Trello/Notion/GitHub issues.

**Integration Considerations:**

* Output a fixed top-K candidate list (e.g., 50) for Phase 2 to prioritize ML training and testing.
* Ensure all configs are versioned and reproducible.

---

## **Phase 2 – Data Acquisition & Infrastructure**

**Objective:** Build robust data pipeline, storage, and infrastructure to support ML and EDA. Includes top-K subset selection and optional screening API.

**Key Components:**

1. **Source & Pipeline Setup**

   * Alpaca primary trading, IB backup.
   * Historical data: Yahoo, Alpha Vantage, IB, Alpaca.
   * Modular connectors for each provider.
   * Config: `.env` + `config/data_sources.yaml`.
   * **Screening API**: optional (Finviz), YAML-controlled, cached locally.
   * Top-K ML subset: fixed 50 candidates based on volume/liquidity/trendiness metrics.

2. **Data Storage**

   * Raw + adjusted datasets.
   * Partitioning: hybrid ticker/year default; YAML-configurable.
   * Batch downloads: last 5 years for top-K, older on-demand.
   * Adjust prices post-storage.
   * Focus on RTH; extended-hours reserved for Phase 3.

3. **Infrastructure**

   * Parquet files; efficient columnar storage.
   * Versioning: config + metadata only; hash/checksum tracking.
   * Staging cache: batch → clean → validate → append.
   * Refresh: weekly by default; incremental only.
   * Error handling: retries, logs.

4. **Logging**

   * `logs/` folder: pull results, screening, validation errors.
   * Debug mode: detailed batch info.

**Integration Considerations:**

* Config allows switching partitioning, parallel/sequential API pulls.
* Top-K ML subset is fixed for Phase 2 training/testing; dynamic selection can be introduced in Phase 3.
* RTH-only dataset ensures simpler ML features, extended-hours later.

---

## **Phase 3 – Exploratory Data Analysis (EDA)**

**Objective:** Analyze S&P 500 (intraday 5-min bars, 10 years) along **liquidity, volatility, trendiness**, and prepare ML-ready features.

**Key Components:**

1. **Data Setup**

   * Universe: current S&P 500.
   * Timeframe: 10-year intraday 5-min bars (top-K subset prioritized).
   * Preprocessing: adjusted for corporate actions, align trading sessions.
   * Storage: Parquet/columnar, supports batching.

2. **Liquidity Metrics**

   * Dollar Volume (DV), Turnover Ratio (TO), Amihud Illiquidity (ILLIQ).
   * Raw + normalized per-day, per-stock.
   * Slippage model for transaction cost approximation.

3. **Volatility Metrics**

   * Realized Volatility, Skewness, Kurtosis.
   * Daily aggregation, cross-sectional normalization for ML.

4. **Trendiness Metrics**

   * Rolling regression slopes, Hurst exponent, spectral analysis, PCA factor loadings.
   * Rolling-window normalization (1–5 days configurable) for feature stability.
   * Store cross-sectional normalized + raw values.

5. **Bias & Limitation Checks**

   * Survivorship bias, lookahead bias.
   * Compute constraint: ~98M rows; batch processing + Parquet.

6. **EDA Outputs**

   * Plots: liquidity curves, volatility heatmaps, Hurst distributions, PCA scatter.
   * Tables: top/bottom 20 daily by liquidity/volatility/trendiness.
   * Feature library: normalized and raw features ready for ML training.

7. **Integration Considerations**

   * Validate feature stability across regimes.
   * Compute correlations between features (liquidity vs volatility, etc.).
   * Prepare top-K ML subset features for ML ranking model input.
   * Transaction cost function based on Amihud + DV ready for simulation.

---

## **Next Steps / Cross-Phase Integration**

1. **Phase 1 → Phase 2**

   * Use defined top-K subset to prioritize ML training/testing.
   * Ensure all config files (`success_metrics.yaml`, `system_limits.yaml`) are referenced in pipeline setup.

2. **Phase 2 → Phase 3**

   * Provide clean, partitioned, RTH-only datasets for EDA.
   * Screening API results feed top-K subset into feature computation.

3. **Phase 3 → ML Modeling**

   * Features normalized per rolling windows.
   * Transaction cost estimates incorporated.
   * Cross-sectional ranking ready for ML training (relative ranking → absolute prediction).

---

### ✅ **Key Configuration Files Across Phases**

| File                          | Purpose                                                     |
| ----------------------------- | ----------------------------------------------------------- |
| `config/system_limits.yaml`   | storage, runtime, API budgets                               |
| `config/success_metrics.yaml` | Sharpe, turnover, IC, etc.                                  |
| `config/data_sources.yaml`    | API connectors, provider priority, screening filters        |
| `config/storage.yaml`         | partitioning, staging paths, refresh schedule               |
| `config/versioning.yaml`      | metadata, hash/checksum tracking                            |
| `config/eda.yaml`             | rolling window parameters, normalization, feature selection |

---
