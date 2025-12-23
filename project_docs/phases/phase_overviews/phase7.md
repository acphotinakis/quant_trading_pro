# **Phase 7 Integration Plan**

**Backtesting Framework**

### Objectives & Scope

The focus of Phase 7 is to build a robust backtesting engine capable of simulating strategy performance under realistic conditions. This phase will implement daily rebalancing, multi-day holding horizons, and cost-adjusted return calculations. It will also track core portfolio metrics including cumulative returns, Sharpe ratios, drawdowns, and turnover. Stress testing across key market regimes—such as 2008 (financial crisis), 2020 (COVID crash), and 2022 (inflation-driven selloff)—will validate robustness. Deliverables include the backtesting scripts, documentation, and YAML configuration files controlling assumptions such as rebalance frequency, holding period, and cost modeling. The central consideration is whether the backtest should prioritize research flexibility (quick iteration) or production-grade rigor, with the recommendation to design for modularity so both can coexist.

### Universe / Asset Selection

Backtesting will rely on the top-K subset defined in Phase 2, filtered further through liquidity and transaction-cost constraints from Phase 6. Survivorship bias must be carefully addressed by ensuring historical universes reflect actual index constituents at each time point. Deliverables will include constituent lists and notes stored in `data/universe/backtest/`. The open question is whether to extend backtests to ETFs or other equity baskets beyond S&P 500 constituents; for Phase 7, the recommendation is to remain focused on equities to ensure alignment with prior phases.

### Data Sources & APIs

All data required for backtesting will already exist in the project’s data pipeline from Phases 2–6, primarily daily OHLCV, adjusted returns, and execution-cost metrics. No new APIs will be needed. YAML configs in `config/data_sources.yaml` will point to the same data storage structure to maintain consistency. The consideration here is whether to later integrate alternative datasets—such as intraday or macroeconomic series—into the backtesting engine. For Phase 7, only daily RTH data will be used, with extended-hours postponed to future iterations.

### Data Acquisition & Storage

The backtest engine will operate on cleaned and adjusted parquet datasets generated in earlier phases. These will be partitioned by ticker and year, with hash and checksum logs to ensure integrity. Backtest-specific outputs such as portfolio weights, trades, and PnL series will be stored in `data/backtests/` for reproducibility. A decision must be made on whether to store every intermediate rebalance snapshot, which increases transparency but also inflates storage. I recommend storing compressed snapshots of portfolio states at rebalance dates to strike the right balance.

### Feature Engineering / Analysis

Feature engineering in this phase is minimal, as features were developed in earlier phases, but their aggregation into portfolio-level signals is key. This includes translating model scores into position weights, turnover-adjusted portfolios, and scenario-based cost deductions. Deliverables will include CSVs of weighted signals, turnover diagnostics, and plots of portfolio-level exposures. Considerations include whether to enforce sector or single-stock caps at this stage, which I recommend implementing to prevent concentration risk in testing.

### Infrastructure / Pipeline

The backtest engine will be developed as a modular component under `src/backtest/`. It will integrate signals from Phase 5, cost adjustments from Phase 6, and the trading universe from Phase 2, simulating returns with daily or multi-day horizons. YAML configs will control parameters such as rebalance frequency, transaction costs, and position sizing rules. Logging and error handling will ensure transparency during long simulations. The question remains whether to parallelize backtests for multiple parameter sweeps or keep execution sequential; my recommendation is to allow for both by designing a pluggable execution layer.

### Evaluation / Success Metrics

Success will be defined by the ability to compute and analyze performance metrics that mirror institutional standards. This includes Sharpe ratio, drawdowns, turnover, volatility, and information coefficient at the portfolio level. YAML configs will define evaluation parameters, and risk matrices will be generated to summarize outcomes across multiple stress-test regimes. The recommendation is to treat IC as the signal-selection metric (from Phase 5) and Sharpe as the portfolio-level validation metric, ensuring both alignment with research goals and economic feasibility.


### Constraints & Assumptions

Backtesting will assume a retail computing environment and will not initially incorporate intraday execution simulation. Fills will be modeled as VWAP-based with cost penalties derived from Phase 6 assumptions. Only long-only portfolios will be implemented in the baseline, though short-selling can be integrated in later iterations. All backtests will be conducted on daily data covering at least the last 15–20 years, subject to data availability. These constraints must be clearly documented to avoid overinterpretation of results.

### Version Control / Reproducibility

Every backtest run will be tied to a specific configuration file and model hash, with logs and metadata recorded for traceability. Outputs will be stored with unique run IDs, and backtest configurations will be committed to Git alongside experiment logs. A decision remains whether to integrate MLflow or W&B at this stage, but I recommend continuing with the lightweight YAML + logs approach until Phase 8, when ensemble testing and production deployment demand heavier experiment tracking.

### Iteration / Next Steps

Phase 7 outputs cost-adjusted, stress-tested backtest results, which provide the foundation for Phase 8’s portfolio optimization and production readiness. Next steps include refining execution assumptions, extending the backtest to include regime detection, and testing dynamic universe selection. Deliverables will include backlog notes and refined configs, with the recommendation to push three standard cost-scenario tracks—optimistic, base, and pessimistic—into Phase 8 for robust portfolio construction.
