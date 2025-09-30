**Phase 2 – Data Acquisition & Infrastructure**

### **Objectives & Scope**

Phase 2 focuses on building a **robust, modular data pipeline and storage infrastructure** to support machine learning and EDA. Key objectives include acquiring historical and intraday 5-min OHLCV data for the S&P 500, selecting a fixed top-K subset of 50 stocks for ML training/testing, and optionally integrating a screening API (e.g., Finviz) for enhanced filtering. Deliverables include pipeline scripts (`src/data/pipeline.py`), YAML configuration files (`config/data_sources.yaml`, `.env`), and cached datasets. Considerations include deciding which provider is primary versus backup, whether to support modular connectors for future expansion, and how strictly to enforce the top-K subset selection at this stage versus making it dynamic in Phase 3.

---

### **Universe / Asset Selection**

The Phase 2 universe continues to focus on the **current S&P 500 constituents**, with priority given to the fixed top-K subset of 50 candidates based on volume, liquidity, and trendiness metrics derived from Phase 1. Deliverables include CSV snapshots of the top-K subset (`data/universe/topK_50.csv`) and documentation of inclusion criteria (`docs/topK_selection_notes.md`). Considerations include how to handle changes in the S&P 500 constituents, whether to maintain historical top-K selections for backtesting, and ensuring that smaller-cap or less-liquid stocks do not inadvertently enter the top-K subset.

---

### **Data Sources & APIs**

Phase 2 evaluates and implements **primary and backup data providers**. Alpaca serves as the primary source for intraday data, with Interactive Brokers (IB) as backup. Historical OHLCV data can be pulled from Yahoo Finance, Alpha Vantage, IB, or Alpaca. Deliverables include YAML configuration files (`config/data_sources.yaml`) detailing provider priority, API keys (`.env`), and rate limits. Optional integration of a screening API (Finviz) is controlled via YAML and cached locally. Considerations include rate-limiting strategies, batch vs sequential pulls, fallback behavior for provider downtime, and cost vs reliability trade-offs.

---

### **Data Acquisition & Storage**

Data is retrieved in **batches for the top-K subset** (last 5 years) with older data available on-demand. Datasets include raw and adjusted OHLCV, stored in **Parquet format** with a default hybrid ticker/year partitioning (`data/raw/` and `data/processed/`). Price adjustments (splits/dividends) are applied post-storage. Deliverables include Parquet files, staging cache directories (`staging/`), and hash/checksum logs for verification. Considerations include defining partitioning logic, incremental versus full refresh strategy, and whether to support RTH-only vs extended-hours data (Phase 3 will add extended-hours).

---

### **Feature Engineering / Analysis**

Phase 2 is primarily infrastructural; feature computation is minimal but includes **top-K selection metrics** (volume, liquidity, trendiness). Deliverables include CSVs (`data/processed/topK_metrics.csv`) and metadata describing calculation methods. Considerations include ensuring that these metrics are compatible with Phase 3 feature engineering, defining normalization strategies for future EDA, and validating metric stability across time periods.

---

### **Infrastructure / Pipeline**

The pipeline is designed for **modularity, error handling, and incremental updates**. Parquet storage enables efficient read/write operations, while staging caches allow batch → clean → validate → append workflows. Weekly refresh is default, with retries and logging for failed API calls (`logs/`). Deliverables include Python scripts (`src/data/pipeline.py`), staging directories, and detailed logging for debugging. Considerations include the choice of parallel vs sequential API calls, cache management, and potential bottlenecks with larger batch sizes.

---

### **Evaluation / Success Metrics**

Success metrics focus on **operational robustness** rather than trading performance at this phase. Deliverables include YAML config for refresh schedules and validation checks (`config/refresh.yaml`), along with log files demonstrating complete data pulls. Key metrics include completeness of the top-K dataset, successful hash verification, and error-free batch pulls. Considerations include defining thresholds for acceptable missing data, consistency of top-K selection metrics, and timing constraints for batch processing.

---

### **Constraints & Assumptions**

Phase 2 operates under **retail compute and storage limitations**, with Parquet files optimized for disk space and read/write speed. Assumptions include focusing on RTH-only data, limiting batch sizes to avoid memory overflow, and restricting refresh frequency to weekly. Deliverables include `config/system_limits.yaml` documenting storage and runtime caps. Considerations include balancing refresh frequency against compute load, planning for eventual Phase 3 extended-hours integration, and anticipating network/API failures.

---

### **Version Control / Reproducibility**

All scripts, configs, and datasets are version-controlled via Git. Metadata and hash logs ensure **reproducibility** of each batch download. Deliverables include the Git repository (`/src`, `/config`, `/data`), staging cache logs, and YAML configs for API connectors. Considerations include whether to version datasets fully or only track metadata, ensuring reproducible top-K selection, and documenting API keys and provider versions.

---

### **Iteration / Next Steps**

Phase 2 outputs feed directly into **Phase 3 – EDA & Feature Analysis**. Clean, partitioned Parquet datasets and top-K metrics serve as inputs for liquidity, volatility, and trendiness computations. Key next steps include validating top-K metrics against historical trends, testing batch pipelines for robustness, and confirming storage/partitioning strategy. Deliverables include handoff documentation (`docs/phase2_to_phase3.md`). Considerations include confirming batch validation procedures, ensuring smooth integration with Phase 3 feature computations, and resolving any ambiguities in provider coverage or top-K definitions.

