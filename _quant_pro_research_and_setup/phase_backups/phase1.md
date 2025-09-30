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
