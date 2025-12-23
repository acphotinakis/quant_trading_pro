**Phase 4 – Feature Engineering & Selection**

### **Objectives & Scope**

Phase 4 of Quant Trading Pro is focused on generating a **daily, ML-ready feature set** for the top-K stocks, normalizing these features, testing their stability across rolling windows, and selecting the most predictive and stable features for downstream machine learning models. This phase will also document feature correlations to avoid redundancy and ensure a high-quality input for both relative ranking and absolute prediction models. Deliverables include a Markdown document `docs/phase4_objectives.md` outlining objectives, daily feature datasets in `data/processed/features/`, and a log file `logs/phase4_feature_log.csv` capturing feature computation and pruning events. Considerations include the selection of rolling window lengths (3, 5, or 10 days), normalization methods (rank-based vs z-score), and ensuring the top-K subset remains the computation focus to balance efficiency and model relevance.

---

### **Universe / Asset Selection**

The universe for Phase 4 consists primarily of the **Phase 2 top-K ML subset** (~50 tickers), which is used to compute and store daily features. The full S&P 500 dataset may be maintained offline for cross-sectional scaling or future expansion, but is not processed daily to conserve resources. Deliverables include `data/universe/topk_subset.csv` containing the current top-K candidates and `docs/universe_notes.md` detailing inclusion criteria and handling of delisted or newly added tickers. Key considerations include how to handle incremental additions or deletions in the top-K universe, and maintaining cross-sectional comparability when the universe composition changes over time.

---

### **Data Sources & APIs**

Phase 4 relies on preprocessed OHLCV data and EDA features produced in Phase 2 and Phase 3. While optional external data sources (such as sector indices or sentiment feeds) may be incorporated in later phases, the core focus is on RTH intraday 5-min OHLCV and derived EDA features. Deliverables include references in `config/data_sources.yaml`, the raw OHLCV dataset in `data/raw/`, and processed features in `data/processed/`. Considerations involve ensuring timestamp consistency, alignment of corporate action adjustments, and maintaining modular connector support for future data integration.

---

### **Data Acquisition & Storage**

Processed OHLCV data for the top-K subset is retrieved daily and stored in **columnar Parquet files**, partitioned by `ticker/date` for efficient access. Features are maintained separately in folders for **raw** and **normalized** versions. Deliverables include `data/processed/features/raw/` and `data/processed/features/normalized/`, with computation metadata logged in `logs/phase4_feature_log.csv`. Considerations include incremental updates for daily computation, versioning of staging versus finalized feature sets, and robust handling of missing data or failed computations.

---

### **Feature Engineering / Analysis**

Liquidity metrics (Dollar Volume, Turnover Ratio, Amihud Illiquidity), volatility metrics (Realized Volatility, Skewness, Kurtosis), and trendiness metrics (rolling regression slope, Hurst exponent, spectral analysis, PCA loadings) are computed for each stock daily. Cross-sectional normalization using rank-based methods is applied, with optional parallel z-score normalization for comparative purposes. Rolling-window stability is evaluated over multi-horizons (3, 5, 10 days), and highly correlated features (correlation >0.9) are pruned, with pairs >0.85 documented. Deliverables include daily feature files in `data/processed/features/{ticker}/YYYY-MM-DD.parquet`, metadata in `data/processed/features/feature_metadata.yaml`, and correlation/stability plots. Considerations involve choosing appropriate rolling windows, normalization method, and thresholds for pruning correlated features while maintaining predictive diversity.

---

### **Infrastructure / Pipeline**

Feature computation is implemented via modular Python scripts (`src/data/phase4_pipeline.py`) supporting parallel processing per ticker while respecting CPU and memory constraints. A **staging cache** handles computation → validation → append steps, and all operations are logged in `logs/phase4_feature_log.csv`. Partitioning and refresh schedules are configurable via `config/storage.yaml`. Key considerations include ensuring parallelization does not exceed memory limits, checkpointing for failed computations, and incremental processing to maintain daily update efficiency.

---

### **Evaluation / Success Metrics**

Features are evaluated based on predictive power, rolling-window stability, and redundancy avoidance. Metrics include Information Coefficient (IC) for relative ranking, rolling correlation of features across windows (>0.7–0.75 stability target), and correlation thresholds ≤0.9 for inclusion. Deliverables include `logs/phase4_metrics.csv` and visualizations such as feature stability heatmaps and correlation matrices. Considerations involve prioritizing stable features over temporarily high-predictive but volatile metrics and ensuring cross-sectional diversity to avoid model overfitting.

---

### **Constraints & Assumptions**

Phase 4 assumes **retail compute limitations** (~16–32 GB RAM, 8–16 cores). Daily feature updates are computed for the top-K subset only, with full S&P 500 datasets maintained offline for reference or later expansion. Focus is on RTH OHLCV data, while extended-hours data will be integrated in future phases. External APIs are minimized to maintain pipeline speed. Key considerations include balancing the computational load with feature completeness and ensuring reproducibility within these resource constraints.

---

### **Version Control / Reproducibility**

Feature metadata (`feature_metadata.yaml`) captures normalization methods, rolling windows, correlation thresholds, and pruning decisions. Raw and normalized feature files are validated via hash/checksum tracking. Git manages all pipeline code and configurations, while `logs/phase4_feature_log.csv` ensures experiment traceability. Deliverables include `config/versioning.yaml` and the full logs folder. Recommendations include explicit tracking of rolling window lengths, normalization method, and correlation thresholds for reproducibility in downstream ML training.

---

### **Iteration / Next Steps**

Phase 4 outputs (daily normalized and raw features) feed directly into the ML pipeline (Phase 5) for ranking and absolute prediction. Key next steps include ongoing monitoring of IC and rolling stability, iterative refinement of feature selection thresholds, and optionally integrating extended-hours data or external datasets for enhanced predictive power. Deliverables include prepared ML-ready features in `data/processed/features/` and documentation for ML objectives in `docs/phase5_objectives.md`. Considerations include refining feature selection criteria based on backtesting results and ensuring seamless cross-phase integration for model development.
