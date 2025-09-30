**Phase 1 – Research & Scoping**

### **Objectives & Scope**

Phase 1 of Quant Trading Pro establishes the foundation of the project by defining its **objectives, scope, and success metrics**. The main goals include predicting daily stock rankings for U.S. equities based on liquidity, volatility, and trendiness, with a trading horizon of 3–10 days, and accommodating retail compute and API limitations. Deliverables include `docs/project_objectives.md` documenting the goals in plain English and `config/success_metrics.yaml` containing primary metrics (Sharpe ratio, turnover-adjusted Sharpe) and secondary metrics (max drawdown, hit rate, feature stability). Considerations include clarifying the scope of the initial universe (S&P 500 only vs ETFs later), defining multi-day ranking horizons, and specifying the level of detail for success metrics that will guide downstream phases.

---

### **Universe / Asset Selection**

The initial universe is the **current S&P 500 constituents**, with the full snapshot stored in `data/universe/sp500_constituents.csv`. Notes on inclusion, corporate actions, and survivorship considerations are maintained in `docs/universe_notes.md`. Deliverables include clear documentation of which tickers are included, any exclusions, and reasoning behind them. Considerations include handling delisted or newly added stocks, potential bias introduced by only using current constituents, and whether to include ETFs or sector indices for later expansion.

---

### **Data Sources & APIs**

Phase 1 evaluates historical and real-time data providers such as **Yahoo Finance, Alpaca, Interactive Brokers (IB), and FMP**, including both coverage and reliability. Deliverables include `docs/data_sources.md`, which contains comparative tables of coverage (intraday 5-min bars, history length), reliability (missing data, corrections), API limits, and costs. Additionally, example plots are produced showing OHLCV discrepancies for a sample ticker across providers. Considerations involve deciding primary vs backup providers, rate-limit implications, data correction protocols, and provider cost vs reliability trade-offs.

---

### **Data Acquisition & Storage**

Although no active acquisition occurs in Phase 1, storage considerations are documented to inform later phases. The maximum committed storage (e.g., 200GB local), maximum runtime per job (e.g., 2 hours), and API call budget are captured in `config/system_limits.yaml`. Considerations include defining storage partitioning strategies (ticker/year vs hybrid), deciding whether raw + cleaned datasets should be stored separately from the outset, and ensuring future scalability within retail hardware constraints.

---

### **Constraints & Assumptions**

Phase 1 codifies system limitations and operational assumptions. These include storage caps, runtime limits, API usage limits, and trade-offs forced by these constraints (e.g., limiting 5-min OHLCV history to 10 years for the S&P 500). Deliverables include `docs/constraints.md` and `config/system_limits.yaml`. Key considerations include balancing dataset completeness vs compute feasibility, clearly communicating limitations to downstream phases, and anticipating edge cases such as extended-hour data or corporate action adjustments.

---

### **Evaluation / Success Metrics**

Success is defined in both operational and analytical terms. Operational metrics include whether the repository, configs, and universe are fully prepared and version-controlled. Analytical metrics include threshold levels for Sharpe ratio, turnover-adjusted Sharpe, and feature stability as documented in `docs/strategy_success.md`. Risk is captured in `docs/risk_matrix.md`, detailing mitigation strategies for **data gaps**, **compute overload**, and **overfitting**. Considerations include defining target thresholds, choosing primary vs secondary metrics, and determining the level of rigor required for risk management documentation.

### **Infrastructure / Pipeline**

Phase 1 sets up project infrastructure for reproducibility and future automation. This includes initializing a Git repository with `/docs`, `/config`, and `/data/universe` folders, preparing `docs/project_timeline.md` for the overall phase plan, and optionally integrating task management tools (Trello, Notion, GitHub issues). Deliverables include the structured repo, timeline document, and any initial issue templates. Considerations include deciding the granularity of task tracking, integration with later data pipelines, and documentation standards to maintain cross-phase consistency.

### **Constraints & Assumptions**

Phase 1 is bounded by **retail compute and storage constraints**, requiring careful planning for dataset size, API usage, and runtime expectations. Assumptions include focusing on current S&P 500 constituents, using intraday 5-min data where feasible, and deferring extended-hours or external datasets to later phases. Deliverables include the documented assumptions in `docs/constraints.md`. Considerations involve ensuring these constraints are communicated clearly to avoid infeasible requests in Phase 2 and Phase 3.

### **Version Control / Reproducibility**

All project artifacts (docs, configs, and universe lists) are version-controlled via Git. Reproducibility is reinforced by storing system limits and success metrics in structured YAML files, ensuring that subsequent phases can reliably reference initial assumptions. Deliverables include a Git repo with `/docs`, `/config`, `/data/universe`, and logs if needed. Considerations include tracking any changes to the universe or metrics that could affect downstream reproducibility.

### **Iteration / Next Steps**

Phase 1 outputs feed directly into **Phase 2 – Data Acquisition & Infrastructure**, providing the universe definitions, selected data providers, and system constraints that shape pipeline design. Key next steps include finalizing top-K candidate selection criteria, referencing success metrics in Phase 2 pipeline configs, and verifying storage and runtime plans against retail compute resources. Deliverables include a documented handoff in `docs/phase1_to_phase2.md`. Considerations include clarifying any uncertainties in universe composition, data provider priority, and constraints before Phase 2 begins.


**Phase 2 – Data Acquisition & Infrastructure**

### **Objectives & Scope**

Phase 2 focuses on building a **robust, modular data pipeline and storage infrastructure** to support machine learning and EDA. Key objectives include acquiring historical and intraday 5-min OHLCV data for the S&P 500, selecting a fixed top-K subset of 50 stocks for ML training/testing, and optionally integrating a screening API (e.g., Finviz) for enhanced filtering. Deliverables include pipeline scripts (`src/data/pipeline.py`), YAML configuration files (`config/data_sources.yaml`, `.env`), and cached datasets. Considerations include deciding which provider is primary versus backup, whether to support modular connectors for future expansion, and how strictly to enforce the top-K subset selection at this stage versus making it dynamic in Phase 3.

### **Universe / Asset Selection**

The Phase 2 universe continues to focus on the **current S&P 500 constituents**, with priority given to the fixed top-K subset of 50 candidates based on volume, liquidity, and trendiness metrics derived from Phase 1. Deliverables include CSV snapshots of the top-K subset (`data/universe/topK_50.csv`) and documentation of inclusion criteria (`docs/topK_selection_notes.md`). Considerations include how to handle changes in the S&P 500 constituents, whether to maintain historical top-K selections for backtesting, and ensuring that smaller-cap or less-liquid stocks do not inadvertently enter the top-K subset.

### **Data Sources & APIs**

Phase 2 evaluates and implements **primary and backup data providers**. Alpaca serves as the primary source for intraday data, with Interactive Brokers (IB) as backup. Historical OHLCV data can be pulled from Yahoo Finance, Alpha Vantage, IB, or Alpaca. Deliverables include YAML configuration files (`config/data_sources.yaml`) detailing provider priority, API keys (`.env`), and rate limits. Optional integration of a screening API (Finviz) is controlled via YAML and cached locally. Considerations include rate-limiting strategies, batch vs sequential pulls, fallback behavior for provider downtime, and cost vs reliability trade-offs.

### **Data Acquisition & Storage**

Data is retrieved in **batches for the top-K subset** (last 5 years) with older data available on-demand. Datasets include raw and adjusted OHLCV, stored in **Parquet format** with a default hybrid ticker/year partitioning (`data/raw/` and `data/processed/`). Price adjustments (splits/dividends) are applied post-storage. Deliverables include Parquet files, staging cache directories (`staging/`), and hash/checksum logs for verification. Considerations include defining partitioning logic, incremental versus full refresh strategy, and whether to support RTH-only vs extended-hours data (Phase 3 will add extended-hours).

### **Feature Engineering / Analysis**

Phase 2 is primarily infrastructural; feature computation is minimal but includes **top-K selection metrics** (volume, liquidity, trendiness). Deliverables include CSVs (`data/processed/topK_metrics.csv`) and metadata describing calculation methods. Considerations include ensuring that these metrics are compatible with Phase 3 feature engineering, defining normalization strategies for future EDA, and validating metric stability across time periods.

### **Infrastructure / Pipeline**

The pipeline is designed for **modularity, error handling, and incremental updates**. Parquet storage enables efficient read/write operations, while staging caches allow batch → clean → validate → append workflows. Weekly refresh is default, with retries and logging for failed API calls (`logs/`). Deliverables include Python scripts (`src/data/pipeline.py`), staging directories, and detailed logging for debugging. Considerations include the choice of parallel vs sequential API calls, cache management, and potential bottlenecks with larger batch sizes.

### **Evaluation / Success Metrics**

Success metrics focus on **operational robustness** rather than trading performance at this phase. Deliverables include YAML config for refresh schedules and validation checks (`config/refresh.yaml`), along with log files demonstrating complete data pulls. Key metrics include completeness of the top-K dataset, successful hash verification, and error-free batch pulls. Considerations include defining thresholds for acceptable missing data, consistency of top-K selection metrics, and timing constraints for batch processing.

### **Constraints & Assumptions**

Phase 2 operates under **retail compute and storage limitations**, with Parquet files optimized for disk space and read/write speed. Assumptions include focusing on RTH-only data, limiting batch sizes to avoid memory overflow, and restricting refresh frequency to weekly. Deliverables include `config/system_limits.yaml` documenting storage and runtime caps. Considerations include balancing refresh frequency against compute load, planning for eventual Phase 3 extended-hours integration, and anticipating network/API failures.

### **Version Control / Reproducibility**

All scripts, configs, and datasets are version-controlled via Git. Metadata and hash logs ensure **reproducibility** of each batch download. Deliverables include the Git repository (`/src`, `/config`, `/data`), staging cache logs, and YAML configs for API connectors. Considerations include whether to version datasets fully or only track metadata, ensuring reproducible top-K selection, and documenting API keys and provider versions.

### **Iteration / Next Steps**

Phase 2 outputs feed directly into **Phase 3 – EDA & Feature Analysis**. Clean, partitioned Parquet datasets and top-K metrics serve as inputs for liquidity, volatility, and trendiness computations. Key next steps include validating top-K metrics against historical trends, testing batch pipelines for robustness, and confirming storage/partitioning strategy. Deliverables include handoff documentation (`docs/phase2_to_phase3.md`). Considerations include confirming batch validation procedures, ensuring smooth integration with Phase 3 feature computations, and resolving any ambiguities in provider coverage or top-K definitions.

**Phase 3 – Exploratory Data Analysis (EDA)**

### **Objectives & Scope**

Phase 3 aims to **analyze S&P 500 intraday data** to compute and validate ML-ready features based on **liquidity, volatility, and trendiness**. This phase builds on the datasets and top-K subset generated in Phase 2 and prepares inputs for the feature engineering and ML ranking pipelines in Phase 4. Deliverables include processed feature CSVs (`data/processed/eda_features.csv`), plots and tables (`plots/`), and configuration files (`config/eda.yaml`). Considerations include determining the **rolling window lengths** for trendiness metrics, defining normalization strategies (cross-sectional vs per-stock), and balancing feature detail against storage/computation limits.

### **Universe / Asset Selection**

The universe remains the **current S&P 500**, with priority given to the **top-K subset of 50 stocks** identified in Phase 2. Deliverables include CSV snapshots of the full universe (`data/universe/sp500_constituents.csv`) and top-K metrics (`data/processed/topK_metrics.csv`). Considerations include handling survivorship bias (only current members are analyzed) and aligning the top-K selection dynamically with EDA results for robustness checks.

### **Data Sources & APIs**

Phase 3 relies on **data retrieved and stored in Phase 2**, including RTH-only 5-min OHLCV data from Alpaca, IB, Yahoo Finance, or Alpha Vantage. Deliverables include local Parquet datasets (`data/processed/`) and YAML configs documenting provider priority and refresh metadata (`config/data_sources.yaml`). Considerations include validating data consistency across providers, ensuring corporate actions adjustments are applied, and confirming the integrity of batch-loaded top-K subset data.

### **Data Acquisition & Storage**

EDA uses **10-year intraday datasets** stored in Parquet format, supporting **batch processing** to handle ~98M rows efficiently. Preprocessing ensures alignment of trading sessions, adjustments for splits/dividends, and exclusion of extended-hours (reserved for Phase 4 or Phase 3 optional experiments). Deliverables include cleaned Parquet files (`data/processed/eda/`), staging logs, and metadata for reproducibility. Considerations include batch size tuning, memory optimization, and ensuring cross-phase compatibility with Phase 4 feature engineering.

### **Feature Engineering / Analysis**

Phase 3 computes **liquidity, volatility, and trendiness metrics**:

* Liquidity: Dollar Volume (DV), Turnover Ratio (TO), Amihud Illiquidity (ILLIQ), including slippage-adjusted cost approximation.
* Volatility: Realized volatility, skewness, kurtosis, daily aggregation, cross-sectional normalization.
* Trendiness: Rolling regression slopes, Hurst exponent, spectral analysis, PCA factor loadings, with **rolling-window normalization** (configurable 1–5 days).

Deliverables include normalized and raw CSVs (`data/processed/eda_features.csv`), correlation tables (`data/processed/feature_correlations.csv`), and plots (`plots/`). Considerations include avoiding multicollinearity, defining stability thresholds, and selecting rolling windows that balance sensitivity to trends versus noise.

### **Infrastructure / Pipeline**

The EDA pipeline leverages **batch-parallel processing**, Parquet columnar storage, and staging caches from Phase 2. Scripts (`src/features/eda_pipeline.py`) automate feature computation, normalization, and storage. Logging captures feature generation status, errors, and metadata. Deliverables include pipeline scripts, staging directories, and logs (`logs/eda/`). Considerations include compute allocation for large batches, incremental updates for new data, and error handling for partial feature failures.

### **Evaluation / Success Metrics**

Success metrics measure **feature quality and stability**, rather than trading performance at this stage. Deliverables include:

* Rank correlation tables across rolling windows.
* Cross-sectional feature stability reports.
* Feature distribution and correlation plots.

Considerations include defining thresholds for acceptable feature instability, monitoring multicollinearity, and ensuring top-K subset metrics remain consistent across regimes.

### **Constraints & Assumptions**

Phase 3 assumes **retail-level compute limits**, with batch processing to handle large datasets. Only **RTH data** is used, and storage is partitioned by ticker/year. Deliverables include `config/system_limits.yaml` documenting memory, runtime, and disk usage. Considerations include balancing feature granularity with compute/memory constraints and planning for eventual extended-hours analysis in Phase 4.

### **Version Control / Reproducibility**

All EDA scripts, configs, and datasets are **version-controlled via Git**, with metadata, staging logs, and hash/checksum verification to ensure reproducibility. Deliverables include Git repository (`/src`, `/config`, `/data`), logs folder (`logs/eda/`), and configuration files (`config/eda.yaml`). Considerations include documenting all feature transformations, storing feature correlation outputs, and maintaining reproducible top-K selection across phases.

### **Iteration / Next Steps**

Phase 3 outputs feed into **Phase 4 – Feature Engineering & Selection**, providing normalized and raw features for ML ranking models. Key next steps include validating rolling-window stability, selecting high-predictive-power features, documenting correlations to avoid redundancy, and preparing data pipelines for automated ML input. Deliverables include handoff documentation (`docs/phase3_to_phase4.md`) and updated YAML configs for feature parameters. Considerations include ensuring seamless integration with Phase 4, confirming stability thresholds, and resolving any remaining gaps in top-K coverage.

**Phase 4 – Feature Engineering & Selection**

### **Objectives & Scope**

Phase 4 of Quant Trading Pro is focused on generating a **daily, ML-ready feature set** for the top-K stocks, normalizing these features, testing their stability across rolling windows, and selecting the most predictive and stable features for downstream machine learning models. This phase will also document feature correlations to avoid redundancy and ensure a high-quality input for both relative ranking and absolute prediction models. Deliverables include a Markdown document `docs/phase4_objectives.md` outlining objectives, daily feature datasets in `data/processed/features/`, and a log file `logs/phase4_feature_log.csv` capturing feature computation and pruning events. Considerations include the selection of rolling window lengths (3, 5, or 10 days), normalization methods (rank-based vs z-score), and ensuring the top-K subset remains the computation focus to balance efficiency and model relevance.

### **Universe / Asset Selection**

The universe for Phase 4 consists primarily of the **Phase 2 top-K ML subset** (~50 tickers), which is used to compute and store daily features. The full S&P 500 dataset may be maintained offline for cross-sectional scaling or future expansion, but is not processed daily to conserve resources. Deliverables include `data/universe/topk_subset.csv` containing the current top-K candidates and `docs/universe_notes.md` detailing inclusion criteria and handling of delisted or newly added tickers. Key considerations include how to handle incremental additions or deletions in the top-K universe, and maintaining cross-sectional comparability when the universe composition changes over time.

### **Data Sources & APIs**

Phase 4 relies on preprocessed OHLCV data and EDA features produced in Phase 2 and Phase 3. While optional external data sources (such as sector indices or sentiment feeds) may be incorporated in later phases, the core focus is on RTH intraday 5-min OHLCV and derived EDA features. Deliverables include references in `config/data_sources.yaml`, the raw OHLCV dataset in `data/raw/`, and processed features in `data/processed/`. Considerations involve ensuring timestamp consistency, alignment of corporate action adjustments, and maintaining modular connector support for future data integration.

### **Data Acquisition & Storage**

Processed OHLCV data for the top-K subset is retrieved daily and stored in **columnar Parquet files**, partitioned by `ticker/date` for efficient access. Features are maintained separately in folders for **raw** and **normalized** versions. Deliverables include `data/processed/features/raw/` and `data/processed/features/normalized/`, with computation metadata logged in `logs/phase4_feature_log.csv`. Considerations include incremental updates for daily computation, versioning of staging versus finalized feature sets, and robust handling of missing data or failed computations.

### **Feature Engineering / Analysis**

Liquidity metrics (Dollar Volume, Turnover Ratio, Amihud Illiquidity), volatility metrics (Realized Volatility, Skewness, Kurtosis), and trendiness metrics (rolling regression slope, Hurst exponent, spectral analysis, PCA loadings) are computed for each stock daily. Cross-sectional normalization using rank-based methods is applied, with optional parallel z-score normalization for comparative purposes. Rolling-window stability is evaluated over multi-horizons (3, 5, 10 days), and highly correlated features (correlation >0.9) are pruned, with pairs >0.85 documented. Deliverables include daily feature files in `data/processed/features/{ticker}/YYYY-MM-DD.parquet`, metadata in `data/processed/features/feature_metadata.yaml`, and correlation/stability plots. Considerations involve choosing appropriate rolling windows, normalization method, and thresholds for pruning correlated features while maintaining predictive diversity.

### **Infrastructure / Pipeline**

Feature computation is implemented via modular Python scripts (`src/data/phase4_pipeline.py`) supporting parallel processing per ticker while respecting CPU and memory constraints. A **staging cache** handles computation → validation → append steps, and all operations are logged in `logs/phase4_feature_log.csv`. Partitioning and refresh schedules are configurable via `config/storage.yaml`. Key considerations include ensuring parallelization does not exceed memory limits, checkpointing for failed computations, and incremental processing to maintain daily update efficiency.

### **Evaluation / Success Metrics**

Features are evaluated based on predictive power, rolling-window stability, and redundancy avoidance. Metrics include Information Coefficient (IC) for relative ranking, rolling correlation of features across windows (>0.7–0.75 stability target), and correlation thresholds ≤0.9 for inclusion. Deliverables include `logs/phase4_metrics.csv` and visualizations such as feature stability heatmaps and correlation matrices. Considerations involve prioritizing stable features over temporarily high-predictive but volatile metrics and ensuring cross-sectional diversity to avoid model overfitting.

### **Constraints & Assumptions**

Phase 4 assumes **retail compute limitations** (~16–32 GB RAM, 8–16 cores). Daily feature updates are computed for the top-K subset only, with full S&P 500 datasets maintained offline for reference or later expansion. Focus is on RTH OHLCV data, while extended-hours data will be integrated in future phases. External APIs are minimized to maintain pipeline speed. Key considerations include balancing the computational load with feature completeness and ensuring reproducibility within these resource constraints.

### **Version Control / Reproducibility**

Feature metadata (`feature_metadata.yaml`) captures normalization methods, rolling windows, correlation thresholds, and pruning decisions. Raw and normalized feature files are validated via hash/checksum tracking. Git manages all pipeline code and configurations, while `logs/phase4_feature_log.csv` ensures experiment traceability. Deliverables include `config/versioning.yaml` and the full logs folder. Recommendations include explicit tracking of rolling window lengths, normalization method, and correlation thresholds for reproducibility in downstream ML training.

### **Iteration / Next Steps**

Phase 4 outputs (daily normalized and raw features) feed directly into the ML pipeline (Phase 5) for ranking and absolute prediction. Key next steps include ongoing monitoring of IC and rolling stability, iterative refinement of feature selection thresholds, and optionally integrating extended-hours data or external datasets for enhanced predictive power. Deliverables include prepared ML-ready features in `data/processed/features/` and documentation for ML objectives in `docs/phase5_objectives.md`. Considerations include refining feature selection criteria based on backtesting results and ensuring seamless cross-phase integration for model development.

# *Phase 5: Modeling & Signal Development**

In **Objectives & Scope**, Phase 5 is designed to transform engineered features from earlier phases into predictive ranking models that generate actionable trading signals. The measurable goal is to achieve robust cross-sectional stock rankings validated through Information Coefficient (IC) and turnover-adjusted Sharpe ratio. Deliverables include documentation (`docs/phase5_objectives.md`) and a fully integrated modeling framework that can toggle across baseline and advanced models. The key consideration is ensuring models balance interpretability, computational cost, and predictive performance.

For **Universe / Asset Selection**, this phase continues to focus on the S&P 500, or a configurable top-K subset defined earlier in Phase 2. Tickers are pulled from a centralized CSV file (`data/universe/sp500_constituents.csv`) and linked to processed feature sets. Considerations here include survivorship bias (ensuring only historically valid constituents are used in backtests) and whether subsets should remain static (fixed top-K) or evolve dynamically later.

Under **Data Sources & APIs**, Phase 5 leverages features and metrics generated in Phases 2 and 3, with no new raw market data introduced at this stage. Configurations for modeling sources are kept in `config/models.yaml`, which defines model families and hyperparameters. Considerations include ensuring alignment between preprocessed data formats and model input requirements, as well as controlling for temporal leakage during feature ingestion.

For **Data Acquisition & Storage**, modeling consumes Parquet or Feather-optimized feature datasets generated in earlier phases. The pipeline ensures partitioning by ticker and date, with versioning handled through hash tracking and metadata logs. Cleaned features are stored in `data/processed/features/` and linked directly into modeling scripts. Considerations here involve ensuring raw vs adjusted feature versions are distinguishable and supporting batch vs rolling window access patterns for training.

Within **Feature Engineering / Analysis**, Phase 5 makes heavy use of liquidity, volatility, and trendiness metrics already defined in Phase 3. Additional transformations include cross-sectional normalization, lagging features to prevent lookahead bias, and rolling-window stability checks. Deliverables include plots of IC over time, tables of feature importance, and a finalized library of normalized features stored in `data/processed/ml_ready/`. Considerations include whether to adopt pairwise ranking losses early or stick with regression + rank conversion for simplicity, as well as validating that engineered features remain stable across different market regimes.

The **Infrastructure / Pipeline** component introduces modular model wrappers in `src/models/`, including baseline logistic and ridge regression, gradient-boosted trees (LightGBM/XGBoost), optional LambdaMART for direct ranking, and ensembles of weak learners. A GPU-enabled path is prepared for sequence-based models (LSTM/Transformer), but these are only deployed if gradient boosting saturates performance. Caching, error handling, and logs (`logs/model_training/`) are built into the training pipeline. Considerations include CPU-first workflows for cost efficiency and a flexible YAML-driven toggle for model selection.

In **Evaluation / Success Metrics**, IC and Rank IC are established as the **primary development metrics**, ensuring the models align with the ranking objective. Sharpe ratio and turnover-adjusted PnL are designated as **secondary business validation metrics** to confirm economic value. Deliverables include `src/evaluation/metrics.py`, YAML configs for thresholds, and `reports/model_eval.md` containing plots, tables, and commentary. The main consideration is that strong IC is necessary but not sufficient — Sharpe validation ensures the signals have tradable value.

The **Constraints & Assumptions** for Phase 5 include prioritizing retail-level compute environments. CPU suffices for logistic regression, ridge, and GBM training, while GPU planning is in place but postponed until sequence models are required. Time splits are handled strictly temporally to avoid leakage, with a default walk-forward expanding window configuration. Assumptions include focusing only on regular trading hours (RTH) and a manageable dataset size due to earlier storage and batching strategies.

For **Version Control / Reproducibility**, every model run is tied to a config and metadata snapshot. GitHub manages code versioning, while training logs and metrics outputs are stored in `logs/model_training/`. Full dataset versioning is avoided to conserve storage; instead, hash tracking ensures that models can be traced back to the exact feature inputs used. Considerations include whether to eventually integrate external experiment tracking (e.g., MLflow or W&B), though Phase 5 proceeds with lightweight YAML + logs.

Finally, in **Iteration / Next Steps**, Phase 5 sets the foundation for Phase 6 (Backtesting & Portfolio Construction). Once models demonstrate stable IC and positive Sharpe proxy, their predictions will be converted into portfolio weights and tested against historical trading simulations. Unresolved questions at this stage include whether pairwise ranking losses should be prioritized later and how to balance the tradeoff between predictive strength and turnover costs. Deliverables include `docs/phase5_next_steps.md`, linking directly into Phase 6 requirements.


# **Phase 6 Integration Plan**

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

