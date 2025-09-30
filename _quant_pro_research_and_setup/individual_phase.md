Now, review my feedback below for all of the clarifying questions. 
Then ask me follow up questions. remember you need to think about this project as if you're a quantitative machine learning expert working at a big quant firm such as jump trading, citadel, optiver but keep in mind that we have the compute power of a retail trader
Once you do this, recreate the phase plans for phases 1, 2, and 3. 

# **Phase Analysis & Observations**

## **Phase 2 – Data Acquisition & Infrastructure**

**Potential Clarifying Questions / Decisions for Phase 2:**

1. **Stock Screening API – Extended-Hours Data**
    [FEEDBACK]
    Allow the user to configure using extended-hours for Stock-Screening API. This by default will be false.
2. **Screening API – Multiple Providers in Parallel**
    [FEEDBACK]
    Just leave this to use one screener for now, which will be the Finviz API screener

3. **Cache Expiration / Refresh**
    [FEEDBACK]
    Use default as a weekly refresh but we could update this later.

4. **Top-K vs Full Universe for ML**
    [FEEDBACK]
    

5. **Error Handling / Missing Data Strategy**

   * While retry logic is included, need clear policy: if a ticker fails multiple times, should it be skipped or flagged for manual intervention?

6. **File Storage Partitioning**

   * Partitioning is hybrid (ticker/year) with YAML config option; should we enforce standard convention to avoid misalignment across pipelines?

---

## **Phase 3 – EDA**

**Potential Clarifying Questions / Decisions for Phase 3:**

1. **Normalization / Z-scoring:**

   * Currently planning cross-sectional normalization per day; should we also normalize over rolling windows for trend features (e.g., 3d or 5d slopes)?
   * **Pros:** smoother feature values, better ML stability.
   * **Cons:** may lag real-time signals slightly.

2. **Transaction Cost Model:**

   * Approximate cost uses Amihud + Dollar Volume; should we include turnover ratio for multi-day trades?
   * Pros/cons: adds realism vs added complexity.

3. **Feature Storage:**

   * Ensure features from Phase 3 are stored in a way that aligns with Phase 2 partitioning for efficient ML training (ticker/year + bar-level aggregation).

4. **Survivorship Bias Awareness:**

   * Using only current S&P500 introduces optimistic liquidity and volatility stats. Should we flag features from low-liquidity or thinly traded tickers?

5. **EDA Horizon vs ML Horizon:**

   * EDA considers multi-day trend windows, ML ranking may use shorter horizons (daily). Clarify alignment.

---


## **Follow-Up Questions**

1. For **screening API**, do we want to **allow multiple providers in Phase 2**, or stick to one?
2. For **top-K ML subset**, should it **update daily based on previous ranking**, or remain fixed for training backtests?
3. For **cache refresh**, do we want **weekly default**, or dynamic/triggered refresh based on volatility or events?
4. For **extended-hours data**, confirm if we will **add in Phase 3** only.
5. For **feature normalization in EDA**, should we consider **rolling window normalization** for trendiness metrics?

