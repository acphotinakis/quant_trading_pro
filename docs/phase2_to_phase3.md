# Handoff: Phase 2 to Phase 3

This document marks the completion of Phase 2 and outlines the inputs and expectations for the start of Phase 3: Exploratory Data Analysis (EDA).

## 1. Summary of Phase 2 Deliverables

Phase 2, "Data Acquisition & Infrastructure," has delivered the following key assets:

-   **A Robust Data Pipeline (`src/data/pipeline.py`):**
    -   Connectors for multiple data providers (Alpaca, Yahoo Finance) with a configurable fallback chain.
    -   A "smarter" universe selection mechanism that identifies a **Top-50 stock universe** based on recent average dollar volume.
    -   A parallelized, batch-processing workflow to download historical data efficiently.
    -   Integrated data validation to check for missing data, outliers, and gaps.

-   **Partitioned Historical Data:**
    -   5+ years of 5-minute OHLCV data for the Top-50 universe has been downloaded.
    -   Data is stored in an efficient **Parquet format**.
    -   The data is partitioned by `ticker/year/month/day` under the `data/raw/` directory for fast time-series queries.
    -   Each data file is accompanied by a `.json` metadata file containing checksums and other reproducibility information.

-   **Key Artifacts:**
    -   `data/processed/topK_50.csv`: The list of the 50 stocks selected for analysis.
    -   `reports/data_quality_dashboard.html`: A dynamic report summarizing the success of the latest data acquisition run and the results of the validation checks.
    -   `logs/data_pipeline/`: Detailed logs for debugging and tracking pipeline execution.

## 2. Inputs for Phase 3: Exploratory Data Analysis (EDA)

Phase 3 will build directly on the data acquired in Phase 2. The primary inputs for the EDA phase are:

-   **The partitioned Parquet dataset** located in `data/raw/`. The EDA scripts will need to read data from this directory structure for the tickers listed in `data/processed/topK_50.csv`.
-   **The Top-50 universe list** (`data/processed/topK_50.csv`) to know which tickers to analyze.

## 3. Expectations for Phase 3

The goal of Phase 3 is to compute and validate the core metrics that will drive the ML models. The main tasks will be:

1.  **Load Data:** Write scripts to efficiently load the partitioned 5-minute data for the Top-50 universe.
2.  **Compute Core Metrics:** Based on the project plan, calculate the following for each stock:
    -   **Liquidity Metrics:** Dollar Volume, Turnover Ratio, Amihud Illiquidity, etc.
    -   **Volatility Metrics:** Realized Volatility, Skewness, Kurtosis, etc.
    -   **Trendiness Metrics:** Rolling Regression Slopes, Hurst Exponent, etc.
3.  **Analyze and Visualize:** Create notebooks and scripts to generate plots, correlation tables, and stability reports for these new features.
4.  **Generate Feature Library:** The final deliverable of Phase 3 will be a clean, validated set of features (e.g., in a CSV or Parquet file) ready for use in Phase 4 (Feature Engineering) and Phase 5 (Modeling).
