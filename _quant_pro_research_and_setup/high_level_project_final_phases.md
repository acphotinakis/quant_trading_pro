# 📑 Phase 1 – Research & Scoping Plan

### **1. Objectives & Scope Definition**

* **Deliverables:**

  * `docs/project_objectives.md` → plain-English statement of project goals.

    * Predict daily stock rankings based on liquidity, volatility, and trendiness.
    * Horizon: multi-day (e.g., 3–10 trading days).
    * Market: US equities (start with S&P 500, later expansion).
    * Constraints: retail compute + API limits.
  * `config/success_metrics.yaml` → structured file listing evaluation metrics:

    * Primary: Sharpe ratio, turnover-adjusted Sharpe.
    * Secondary: max drawdown, hit rate, feature stability.

---

### **2. Universe Selection**

* **Deliverables:**

  * `data/universe/sp500_constituents.csv` → snapshot of current S&P 500 tickers.
  * `docs/universe_notes.md` → notes on inclusion/exclusion (e.g., only currently listed names, corporate actions handling).

---

### **3. Data Source Evaluation**

* **Deliverables:**

  * `docs/data_sources.md` → comparison table of Yahoo, Alpaca, IB, FMP. Include:

    * Coverage (intraday 5-min bars, history length).
    * Reliability (missing data, corrections).
    * API limits & costs.
  * **Plots:** example pull of 5-min OHLCV for 1 ticker across providers to visualize discrepancies.

---

### **4. Constraints & Assumptions**

* **Deliverables:**

  * `config/system_limits.yaml` → defines:

    * Max storage we’ll commit (e.g., 200GB local).
    * Max runtime per job (e.g., 2 hrs for backtest).
    * API call budget (per day/week).
  * `docs/constraints.md` → discussion of what tradeoffs this forces (e.g., 5-min data limited to last 10 years for S&P500 only).

---

### **5. Success Criteria & Risk Management**

* **Deliverables:**

  * `docs/risk_matrix.md` → table with risks + mitigations:

    * **Data Gaps** → cross-check with backup provider.
    * **Compute Overload** → reduce universe, aggregate bars.
    * **Overfitting** → strict walk-forward validation.
  * `docs/strategy_success.md` → describes thresholds for moving forward (e.g., Sharpe > 1.2 net of costs in backtests, stable feature importance across rolling windows).

---

### **6. Project Management Setup**

* **Deliverables:**

  * GitHub repo initialized with:

    * `/docs` → project documentation.
    * `/config` → YAML/JSON configs for parameters.
    * `/data/universe` → ticker lists.
  * `docs/project_timeline.md` → rough phase breakdown (1–10) with estimated time per phase.
  * Issue tracker/Trello/Notion setup to assign tasks (even if single-person).

---

# ✅ Phase 1 Completion Checklist

* Project objectives written & version-controlled.
* Universe clearly defined & stored.
* Data providers evaluated with plots + notes.
* System constraints codified in config.
* Success metrics + risk matrix finalized.
* Git repo initialized with docs/config structure.

--- 

# 🔹 Phase 2 – Data Acquisition & Infrastructure (Finalized)

---

## **1. Source & Pipeline Setup**

### a. API Connections

* **Primary / Backup:**

  * Alpaca for trading; Interactive Brokers (IB) as backup.
  * Historical data via Yahoo Finance, Alpha Vantage, IB, and Alpaca.

* **Modular API Connectors:**

  * Each data source is wrapped in a modular connector (Python class or function).
  * Easy to switch provider, implement batching, and support rate-limit awareness.

* **API Key Storage:**

  * `.env` for secrets.
  * `config/data_sources.yaml` for provider selection and configuration.

* **Real-time vs Historical:**

  * Trading pipeline → real-time streaming.
  * ML / EDA → historical batch pulls.

* **Stock Screening API (Optional, user-configurable):**

  * Single provider for Phase 2 (e.g., Finviz screener).
  * Default → full S&P500 for ranking.
  * User override via YAML:

    ```yaml
    screening_enabled: true
    screening_provider: finviz
    screening_filters: {market_cap: ">2B", sector: "Tech"}
    ```
  * Cached locally in `data/screened/` to avoid repeated API calls.

---

### b. Store Intraday 5-min OHLCV Data

* **Data Storage:**

  * Raw + cleaned (adjusted) datasets for reproducibility.
  * Partitioning options: `ticker`, `year/month`, or hybrid (`ticker/year`) — configurable in `config/storage.yaml`.

* **Batch Downloads & On-demand Backfill:**

  * Pull last 5 years first for top-K tickers.
  * Older data pulled on-demand for exploratory analysis or ML experiments.

* **Price Adjustments:**

  * Always store raw first.
  * Adjust for splits/dividends post-storage.

* **Trading Hours:**

  * Phase 2 focus on **regular trading hours (RTH)** only.
  * Extended-hours can be added in Phase 3 for top-K tickers.

---

## **2. Infrastructure**

### a. Efficient Storage (Parquet + Python Scripts)

* **Partitioning:**

  * Default: **hybrid** (ticker + year) → scalable and fast for ML or temporal queries.
  * Configurable via YAML for experimentation.

* **File Format:** Parquet (compressed, efficient for columnar reads).

* **Storage Location:** Local SSD (`data/raw/`, `data/processed/`), cloud optional for future.

---

### b. Version Control & Data Integrity

* **Config + Metadata Versioning:**

  * Tracks provider, pull dates, screening API parameters.
  * Lightweight, reproducible, storage-efficient.

* **Hash / Checksum Tracking:**

  * Validate raw + cleaned datasets.
  * Detect partial downloads, corruption, or accidental modification.

---

### c. Caching & Refresh Logic

* **Staging Cache:**

  1. Download new batch → store in staging.
  2. Clean / adjust prices.
  3. Validate hashes → append to main dataset.

* **Incremental Updates:**

  * Only append new data; rebuild entire dataset only if corruption detected.

* **Refresh Frequency:**

  * Trading data → daily after market close.
  * Historical backfill → weekly.
  * Screening API cache → weekly by default, configurable in YAML.

* **Error Handling:**

  * Retry failed API calls with exponential backoff (configurable max retries).
  * Log failures; skip tickers after max retries.

---

## **3. Logging**

* **Automated Logs:**

  * Stored in `logs/` folder.
  * Timestamped per configuration run.
  * Includes:

    * Pull success/failure
    * Screening tickers used
    * Hash validation results
    * Errors or warnings

* **Granularity:**

  * Default: basic logs.
  * Debug mode: detailed logs including batch sizes, processing time, warnings.

---

## **4. Stock Screening Integration (New)**

* **User-configurable subset selection:**

  * YAML config controls screening API and filters.
  * Cached results to avoid repeated API calls.
  * Used as input for ML training/testing pipelines.

* **Pipeline Flow:**

  * Full S&P500 → optional screening API → top-K ML subset → raw/processed storage → ML training.

---

## **5. Final Deliverables for Phase 2**

| Deliverable                | Description                                                                                                                                   |
| -------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `src/data/pipeline.py`     | Modular connectors for historical/trading data, Finviz screener integration, corporate action adjustments, staging cache, incremental updates |
| `data/raw/`                | Raw OHLCV + adjusted data, per ticker/year                                                                                                    |
| `data/processed/`          | Cleaned + adjusted datasets for EDA & ML                                                                                                      |
| `data/screened/`           | Cached screening API subsets                                                                                                                  |
| `config/data_sources.yaml` | API endpoints, batch/parallel options, provider priority, screening API parameters                                                            |
| `config/storage.yaml`      | Partitioning options, staging paths, refresh frequency, overwrite policy                                                                      |
| `config/versioning.yaml`   | Metadata versioning, hash/checksum tracking, screening API metadata                                                                           |
| `logs/`                    | Run logs: tickers, screening results, hash validation, errors/warnings                                                                        |
| `docs/data_pipeline.md`    | Flowchart, pipeline steps: batch/backfill, staging cache, screening, refresh, error handling                                                  |

---

## **6. Implementation Notes**

* Modular, flexible pipeline supports:

  * Full S&P500 ranking
  * Optional screening API subset
  * Incremental updates + caching
  * Hash validation for reproducibility
  * Configurable partitioning and refresh schedules

* RTH only for Phase 2; extended-hours optional in Phase 3 for top-K tickers.

* Logs + cache ensure reproducibility and traceability across ML runs.

# Phase 3 -  Exploratory Data Analysis Plan – Quant Trading Pro

**Objective:**
Evaluate U.S. equities (S&P 500 initially, intraday 5-min bars, 10 years) along three dimensions: **liquidity, volatility, and trendiness.**
EDA outputs will be used to (1) define feature sets for machine learning models, and (2) model slippage/transaction costs.

---

## 1. **Data Setup**

* **Universe:** Current S&P 500 constituents (survivorship bias noted).
* **Timeframe:** 10 years of intraday 5-min OHLCV bars.
* **Providers:** Interactive Brokers (primary), Yahoo/Alpaca/FMP (secondary).
* **Preprocessing:**

  * Adjust for splits/dividends.
  * Align trading sessions (exclude halts/holidays).
  * Store data in columnar format (Parquet/Feather) for compression.

---

## 2. **Liquidity Analysis**

**Metrics:**

1. **Dollar Volume (DV):**
   [
   DV_t = Close_t \times Volume_t
   ]
   Stored per 5-min bar + daily sum.

2. **Turnover Ratio (TO):**
   [
   TO_t = \frac{Volume_t}{SharesOutstanding}
   ]
   Captures relative liquidity across market caps.

3. **Amihud Illiquidity (ILLIQ):**
   [
   A_t = \frac{|r_t|}{DV_t}, \quad ILLIQ_d = \frac{1}{N_d}\sum_{t=1}^{N_d} A_t
   ]
   where (r_t = \ln(Close_t / Close_{t-1})).
   Stored per 5-min bar + daily average.

**Processing:**

* Store both **raw values** (for slippage modeling) and **cross-sectional normalized values** (z-score or rank per day, for ML features).
* Start with **separate features (DV, TO, Amihud)**; test later whether to combine into a composite liquidity score.

**EDA Tasks:**

* Plot U-shaped intraday liquidity curves.
* Rank stocks daily by liquidity measures.
* Compare sector liquidity distributions.
* Slippage model: approximate cost ≈ (k \times A_t \times TradeSize).

---

## 3. **Volatility Analysis**

**Metrics:**

1. **Realized Volatility (RV):**
   [
   RV_d = \sqrt{\sum_{t=1}^{N_d} r_t^2}
   ]
   Use 5-min returns aggregated daily.

2. **Realized Skewness (RS):**
   [
   RS_d = \frac{1}{N_d} \sum_{t=1}^{N_d} \left(\frac{r_t}{RV_d}\right)^3
   ]

3. **Realized Kurtosis (RK):**
   [
   RK_d = \frac{1}{N_d} \sum_{t=1}^{N_d} \left(\frac{r_t}{RV_d}\right)^4
   ]

**Processing:**

* Compute per-day values.
* Normalize cross-sectionally (z-score) for ML comparability.
* Keep raw values for regime/market structure analysis.

**EDA Tasks:**

* Volatility clustering heatmaps across time of day.
* Sector-level volatility comparisons.
* Regime detection: high-vol vs low-vol periods (COVID, 2022 bear).
* Compare daily realized vol with VIX.

---

## 4. **Trendiness Analysis**

**Metrics:**

1. **Rolling Regression Slope (SLOPE):**
   Regression of log-price vs time over rolling multi-day windows (1d, 3d, 5d).
   Coefficient = trend direction; R² = trend strength.

2. **Hurst Exponent (H):**
   ( H > 0.5 ) = persistence/trending; ( H < 0.5 ) = mean-reversion.

3. **Spectral Analysis (SPEC):**
   Fourier/wavelet decomposition of intraday returns to detect periodicities.

4. **PCA Factor Loadings (PCA):**

   * Run PCA on cross-section of returns.
   * Extract top 3 components (market + major sectors).
   * Trendiness = residual alignment/divergence from these latent factors.

**Processing:**

* Store daily aggregates (multi-day windows roll forward).
* Normalize slope/Hurst/PCA loadings cross-sectionally.

**EDA Tasks:**

* Distribution plots of Hurst exponents across stocks.
* Trend persistence histograms (does a 1-day trend extend to 3-day horizon?).
* PCA scatter plots → sector clustering.
* Compare spectral signatures across sectors.

---

## 5. **Bias & Limitation Checks**

* **Survivorship bias:** No delisted stocks → optimistic liquidity/volatility.
* **Lookahead bias:** Ensure all rolling features lagged appropriately.
* **Compute constraint:** 5-min bars × 500 stocks × 10 yrs ≈ 98M rows → requires efficient storage (Parquet) and batch processing.

---

## 6. **Outputs**

1. **Plots:**

   * Liquidity curves, volatility heatmaps, Hurst histograms, PCA clusters.
2. **Tables:**

   * Top/bottom 20 stocks daily by liquidity/volatility/trendiness.
   * Transaction cost estimates by stock and sector.
3. **Feature Library:**

   * Liquidity: Dollar Vol, Turnover, Amihud (raw + normalized, bar + daily).
   * Volatility: Realized vol, skew, kurtosis (raw + normalized).
   * Trendiness: Slope, Hurst, Spectral, PCA (normalized).

---

## 7. **Next Steps After EDA**

* Validate feature stability across regimes.
* Test correlations between features (e.g., liquidity vs volatility).
* Select a **feature set for ML ranking model**.
* Build a **transaction cost function** using Amihud + DV.


