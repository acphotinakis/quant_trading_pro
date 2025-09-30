**Phase 3 – Exploratory Data Analysis (EDA)**

### **Objectives & Scope**

Phase 3 aims to **analyze S&P 500 intraday data** to compute and validate ML-ready features based on **liquidity, volatility, and trendiness**. This phase builds on the datasets and top-K subset generated in Phase 2 and prepares inputs for the feature engineering and ML ranking pipelines in Phase 4. Deliverables include processed feature CSVs (`data/processed/eda_features.csv`), plots and tables (`plots/`), and configuration files (`config/eda.yaml`). Considerations include determining the **rolling window lengths** for trendiness metrics, defining normalization strategies (cross-sectional vs per-stock), and balancing feature detail against storage/computation limits.

---

### **Universe / Asset Selection**

The universe remains the **current S&P 500**, with priority given to the **top-K subset of 50 stocks** identified in Phase 2. Deliverables include CSV snapshots of the full universe (`data/universe/sp500_constituents.csv`) and top-K metrics (`data/processed/topK_metrics.csv`). Considerations include handling survivorship bias (only current members are analyzed) and aligning the top-K selection dynamically with EDA results for robustness checks.

---

### **Data Sources & APIs**

Phase 3 relies on **data retrieved and stored in Phase 2**, including RTH-only 5-min OHLCV data from Alpaca, IB, Yahoo Finance, or Alpha Vantage. Deliverables include local Parquet datasets (`data/processed/`) and YAML configs documenting provider priority and refresh metadata (`config/data_sources.yaml`). Considerations include validating data consistency across providers, ensuring corporate actions adjustments are applied, and confirming the integrity of batch-loaded top-K subset data.

---

### **Data Acquisition & Storage**

EDA uses **10-year intraday datasets** stored in Parquet format, supporting **batch processing** to handle ~98M rows efficiently. Preprocessing ensures alignment of trading sessions, adjustments for splits/dividends, and exclusion of extended-hours (reserved for Phase 4 or Phase 3 optional experiments). Deliverables include cleaned Parquet files (`data/processed/eda/`), staging logs, and metadata for reproducibility. Considerations include batch size tuning, memory optimization, and ensuring cross-phase compatibility with Phase 4 feature engineering.

---

### **Feature Engineering / Analysis**

Phase 3 computes **liquidity, volatility, and trendiness metrics**:

* Liquidity: Dollar Volume (DV), Turnover Ratio (TO), Amihud Illiquidity (ILLIQ), including slippage-adjusted cost approximation.
* Volatility: Realized volatility, skewness, kurtosis, daily aggregation, cross-sectional normalization.
* Trendiness: Rolling regression slopes, Hurst exponent, spectral analysis, PCA factor loadings, with **rolling-window normalization** (configurable 1–5 days).

Deliverables include normalized and raw CSVs (`data/processed/eda_features.csv`), correlation tables (`data/processed/feature_correlations.csv`), and plots (`plots/`). Considerations include avoiding multicollinearity, defining stability thresholds, and selecting rolling windows that balance sensitivity to trends versus noise.

---

### **Infrastructure / Pipeline**

The EDA pipeline leverages **batch-parallel processing**, Parquet columnar storage, and staging caches from Phase 2. Scripts (`src/features/eda_pipeline.py`) automate feature computation, normalization, and storage. Logging captures feature generation status, errors, and metadata. Deliverables include pipeline scripts, staging directories, and logs (`logs/eda/`). Considerations include compute allocation for large batches, incremental updates for new data, and error handling for partial feature failures.

---

### **Evaluation / Success Metrics**

Success metrics measure **feature quality and stability**, rather than trading performance at this stage. Deliverables include:

* Rank correlation tables across rolling windows.
* Cross-sectional feature stability reports.
* Feature distribution and correlation plots.

Considerations include defining thresholds for acceptable feature instability, monitoring multicollinearity, and ensuring top-K subset metrics remain consistent across regimes.

---

### **Constraints & Assumptions**

Phase 3 assumes **retail-level compute limits**, with batch processing to handle large datasets. Only **RTH data** is used, and storage is partitioned by ticker/year. Deliverables include `config/system_limits.yaml` documenting memory, runtime, and disk usage. Considerations include balancing feature granularity with compute/memory constraints and planning for eventual extended-hours analysis in Phase 4.

---

### **Version Control / Reproducibility**

All EDA scripts, configs, and datasets are **version-controlled via Git**, with metadata, staging logs, and hash/checksum verification to ensure reproducibility. Deliverables include Git repository (`/src`, `/config`, `/data`), logs folder (`logs/eda/`), and configuration files (`config/eda.yaml`). Considerations include documenting all feature transformations, storing feature correlation outputs, and maintaining reproducible top-K selection across phases.

---

### **Iteration / Next Steps**

Phase 3 outputs feed into **Phase 4 – Feature Engineering & Selection**, providing normalized and raw features for ML ranking models. Key next steps include validating rolling-window stability, selecting high-predictive-power features, documenting correlations to avoid redundancy, and preparing data pipelines for automated ML input. Deliverables include handoff documentation (`docs/phase3_to_phase4.md`) and updated YAML configs for feature parameters. Considerations include ensuring seamless integration with Phase 4, confirming stability thresholds, and resolving any remaining gaps in top-K coverage.

