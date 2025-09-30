

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


