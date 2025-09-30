# **Quant Trading Pro – Phase 6 Integration Plan**

**Transaction Cost & Execution Modeling**

### Objectives & Scope

The primary goal of Phase 6 is to incorporate realistic transaction cost estimation and execution-aware modeling into the pipeline. This includes building an Amihud-based slippage model, creating liquidity cost buckets, simulating fill rates, and adjusting signals accordingly. Deliverables will include updated documentation, execution-focused YAML configuration files, and parquet outputs of cost-adjusted scores. A key consideration is whether costs should be modeled at the individual ticker level or generalized into cross-sectional liquidity buckets, which balances specificity against robustness. My recommendation is to begin with generalized buckets for scalability.

### Universe / Asset Selection

This phase uses the same S&P 500 universe, narrowed to the top 50 names from Phase 2, with additional filters based on liquidity. Illiquid tickers may either be excluded entirely or included with penalized signals to reflect higher costs. Deliverables include liquidity flags, exclusion notes, and supporting CSV files. I recommend penalizing rather than excluding illiquid names to preserve optionality while accurately reflecting risk.

### Data Sources & APIs

Transaction cost modeling will rely on the OHLCV and volume data already acquired in earlier phases, specifically Phases 2 and 3. Amihud’s illiquidity measure can be derived from existing return and dollar-volume data, meaning no new APIs or providers are needed for this stage. The open question is whether to eventually enrich this framework with external TAQ or tick-level datasets. For Phase 6, the plan is to remain within daily aggregate proxies to keep costs low and pipelines lightweight.

### Data Acquisition & Storage

Data will be aggregated into daily Amihud illiquidity metrics, spreads, and turnover measures, then partitioned by ticker and date. Outputs will be stored in `data/processed/execution/` with parquet format for efficiency and reproducibility. A decision point here is whether to preserve all raw slippage input variables separately, or to only retain aggregated metrics. I recommend storing raw components alongside aggregates for future flexibility, even if it requires slightly more storage.

### Feature Engineering / Analysis

Execution modeling centers on computing Amihud’s illiquidity ratio (absolute returns divided by dollar volume) and grouping tickers into liquidity buckets, such as quintiles. These buckets will drive both cost simulation and position-sizing rules. Position sizing may follow simple caps based on percentage of average daily volume, or it may evolve into an adaptive system informed by turnover distributions from Phase 5. Initially, I recommend rule-based caps to keep assumptions transparent and testable.

### Infrastructure / Pipeline

A new execution module will be added to `src/execution/`. This module will take Phase 5 signals as inputs, apply slippage and fill simulations, and output cost-adjusted signals. Deliverables include scripts for slippage modeling and fill simulation, YAML configs, and execution logs. A key question is whether slippage should be strictly modeled as a linear function of Amihud × order size or if non-linear functional forms should be introduced. I recommend starting linear for simplicity, with an option to expand later.

### Evaluation / Success Metrics

Evaluation will focus on the distribution of estimated costs across liquidity buckets, the relationship between turnover and cost, and the effect on information coefficient (IC), Sharpe ratios, and backtested PnL. Deliverables will include YAML evaluation configs, plots comparing pre- and post-cost IC, and backtest logs. Success will be defined by whether signals remain profitable under reasonable cost assumptions, such as 5–10 basis points per trade.

### Constraints & Assumptions

The framework assumes a retail environment without access to institutional-grade tick-level data. Execution is modeled as fills around VWAP, adjusted by Amihud-based slippage and capped by ADV participation rules. Only partial fills above 20% ADV will be assumed. Assumptions will be documented in dedicated markdown files. One decision is whether to incorporate extended-hours trading assumptions at this stage, but I recommend deferring this until Phase 7 backtesting.

### Version Control / Reproducibility

All execution model outputs will be tied back to Phase 5 model hashes and configuration files to ensure reproducibility. Metadata will be logged with commit IDs, stored in both logs and JSON metadata files. The team must decide whether to integrate experiment trackers like MLflow or Weights & Biases now, or continue with the lightweight YAML + logs approach. My recommendation is to defer experiment trackers until Phase 7 when multiple backtesting runs are conducted in parallel.

### Iteration / Next Steps

Phase 6 produces cost-adjusted signals, liquidity-aware position sizing, and fill assumptions that directly feed into Phase 7 portfolio backtesting and evaluation. Iteration will involve testing different liquidity bucket sizes, exploring linear versus non-linear slippage models, and tuning position-sizing rules. Deliverables will include transition documentation and backlog notes for unresolved questions. I recommend providing multiple cost scenarios (optimistic, base, pessimistic) to Phase 7 rather than relying on a single set of assumptions.

### Cross-Phase Integration

Phase 6 depends on OHLCV and volume data from Phases 2–3 and the signals generated in Phase 5. Its outputs—cost-adjusted signals, position-sizing adjustments, and execution-aware PnL series—will flow directly into Phase 7. This ensures the project’s signal development pipeline evolves into a realistic portfolio framework that accounts for trading frictions.

