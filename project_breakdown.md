











## 🔍 Breakdown of Phase 1

### 1. **Project Objectives**

* Clarify the goal: Are we trying to **rank stocks for trading**, **forecast returns**, or **construct a portfolio**?
* Define whether the model is for **absolute prediction** (price goes up/down) or **relative ranking** (top-N stocks vs universe).

[ANSWER]
Goal is to rank stocks for trading, use those stocks to train machine learning models to predict which stocks could possibly move for a given trading day, then create another machine learning model to predict direction for that stocks and trade them. We will use relative ranking machine learning to then create a model for absolute prediction to trade

---

### 2. **Universe Definition**

* What assets do we trade first (S&P 500, mid-caps, ETFs)?
[ANSWER] 
Want to focus on S&P 500 and ETFs. But you should critique my answer to this question and walk me through which one to choose with pros and cons.

* Survivorship bias: Do we want historical constituents or just current members?
[ANSWER] 
current members

* Should we include **delisted names** later for robustness?
[ANSWER] 
We can handle this later but ignore for now

---

### 3. **Data Scope & Resolution**

* Horizon: intraday → daily → multi-day?
* Granularity: 5-min bars? daily OHLC? both?
* How much history is enough (10y intraday ≈ huge compute)?
[ANSWER] 
This depends, I'm not sure what horizon to use for EDA vs ranking stocks vs selecting stocks vs training Machine learning models on different horizons when to use a given horizon for either. But you should critique my answer to this question and walk me through which one to choose with pros and cons.

At max we can use 10 years, but based on compute costs and performance, we may have to use 5 years of data but we can change this later. 

---

### 4. **Constraints**

* **Capital assumptions:** Are we modeling as if we have $10k, $100k, or $1M?
[ANSWER] 
Modeling as if we have $25k 

* **Transaction costs:** Flat commission? Per-share? Slippage assumptions?
[ANSWER] 
Assume that we're using Alpaca API or Interactive Brokers for trading so take their own transaction costs into account.

* **Compute/storage:** What’s our realistic budget for data pulls & processing?
[ANSWER] 
Don't worry about this.

---

### 5. **Success Metrics**

* Strategy evaluation: Sharpe ratio, Sortino, CAGR, max drawdown?
[ANSWER] 
Break down each, explain when i'd want to use either of the evaluation metrics or a combination of them. Includes pros and cons and relate your answer to the project overall goal. Ask follow up questions when needed and include your own suggestions given the project overall goal.

* Feature evaluation: Predictive power (IC, rank correlation)?
[ANSWER] 
Break down each, explain when i'd want to use either of the evaluation metrics or a combination of them. Includes pros and cons and relate your answer to the project overall goal. Ask follow up questions when needed and include your own suggestions given the project overall goal.

* Practical evaluation: Liquidity-adjusted returns, turnover constraints?
[ANSWER] 
Break down each, explain when i'd want to use either of the evaluation metrics or a combination of them. Includes pros and cons and relate your answer to the project overall goal. Ask follow up questions when needed and include your own suggestions given the project overall goal.


---

### 6. **Risk & Risk Tolerance**

* Max % of portfolio per stock?
* Max sector exposure?
* Max leverage?
* Acceptable drawdown tolerance?
[ANSWER] 
Break down each, explain when i'd want to use either of the evaluation metrics or a combination of them. Includes pros and cons and relate your answer to the project overall goal. Ask follow up questions when needed and include your own suggestions given the project overall goal.


---

### 7. **Iteration Plan**

* Do we want to:

  * **MVP focus:** Build a small-scale S&P 500 strategy first.
  * **Scalable roadmap:** Expand universe + features later.

[ANSWER]
Scalable roadmap: Expand universe + features later.

---

## ❓ Follow-up Questions for You

1. **Project Objective:**
   Do we want this system to **rank stocks** (like “Top 20” daily/weekly picks) or to **construct a portfolio** directly?
[ANSWER] 
Break down each, explain when i'd want to use either of the evaluation metrics or a combination of them. Includes pros and cons and relate your answer to the project overall goal. Ask follow up questions when needed and include your own suggestions given the project overall goal.


2. **Universe:**
   Should we focus only on **S&P 500 current members** to start, or include **historical constituents** (harder, but avoids survivorship bias)?
[ANSWER] 
S&P 500 current members

3. **Time Horizon:**
   Are we ultimately targeting **short-term (days)**, **swing (weeks)**, or **medium-term (months)** trades?
[ANSWER] 
short-term (days)

4. **Capital Base:**
   What’s the assumed **capital size** we’re trading with (e.g., $10k, $100k, $1M)?
   → This will affect slippage assumptions and whether we can scale strategies.
[ANSWER] 
$25k to $100k


5. **Transaction Costs:**
   Should we model **retail-like costs** (Interactive Brokers per-share commissions, realistic slippage) or assume near-zero costs like HFT firms?
[ANSWER]
retail-like costs


6. **Success Metrics:**
   What matters most: **Sharpe ratio, CAGR, drawdown, win rate, or turnover-adjusted returns**?
[ANSWER] 
Break down each, explain when i'd want to use either of the evaluation metrics or a combination of them. Includes pros and cons and relate your answer to the project overall goal. Ask follow up questions when needed and include your own suggestions given the project overall goal.

7. **Risk Constraints:**
   Are we imagining this strategy with **no leverage (cash only)** or do we want to allow **margin/leverage** in backtests?
[ANSWER]
To start we will use no leverage and then maybe later implement to allow margin/leverage in backtests.

8. **Iteration Style:**
   Would you prefer to:
   * Build a **narrow MVP** (S&P 500, basic features → working pipeline fast), OR
   * Build a **full research platform** first, then iterate on features/models later?

[ANSWER]
Build a full research platform first, then iterate on features/models later





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

---

✅ This plan balances **advanced quant rigor** (Amihud, Hurst, PCA, spectral) with **retail compute feasibility** (5-min bars, efficient storage).

