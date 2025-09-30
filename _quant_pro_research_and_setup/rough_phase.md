# 🔹 Phase 2 – Data Acquisition & Infrastructure (Finalized with Stock Screening)

---

## **1. Source & Pipeline Setup**

### a. API Connections

**Analysis:**

* **Primary/Backup Strategy:** Alpaca primary for trading; IB as backup. Historical data via multiple providers (Yahoo, Alpha Vantage, IB, Alpaca).
* **API Key Storage:** `.env` for secrets, YAML for reference/configuration.
* **Rate-limit Awareness:** Batch requests for 10-year intraday data; modular connectors allow switching providers.
* **Real-time vs Historical:**

  * Trading → real-time streaming.
  * EDA / ML → historical batch pulls.
* **Stock Screening API (New):** Optional API (Finviz screener) allows user-defined filtering (e.g., liquidity, sector, price, market cap) to produce a dynamic subset for ML training.

**Recommendation (Actionable):**

* Modular connectors for each provider including **Finviz screener**.
* API keys stored securely and referenced in YAML.
* Configurable batching, sequential or parallel pulls.
* Screening API integrated as **optional pre-selection** step in pipeline:

  * Default → full S&P500.
  * User can override via `config/data_sources.yaml` (e.g., `use_stock_screener: true`, `screening_provider: finviz`).
* Historical data pulls still support both full S&P500 and user-filtered tickers.

---

### b. Store intraday 5-min OHLCV data

**Analysis:**

* Adjusted prices are critical; implement corporate action adjustments post-pull if provider doesn’t supply.
* Store both raw + cleaned datasets.
* Batch download required; 10-year 5-min bars is large.
* Hybrid on-demand backfill: last 5 years for top tickers first; older data on-demand for exploratory analysis.
* Focus on RTH; extended-hours optional later.

**Recommendation (Actionable):**

* Raw + cleaned datasets stored per ticker/year as Parquet.
* Stock subset selection:

  * Use top K from S&P500 analysis or screening API results.
  * Configurable in YAML: `screening_enabled`, `screening_provider`, `screening_filters`.
* Batch downloads by ticker/year; incremental backfill supported.

---

## **2. Infrastructure**

### a. Efficient Storage (Parquet + Python Scripts)

**Analysis:**

* Partitioning options: Ticker, Year/Month, Hybrid.
* Hybrid (Ticker + Year) balances ML per-stock access and temporal queries.

**Recommendation (Actionable):**

* Store **flat Parquet files**.
* Partitioning configurable:

  * `ticker` only
  * `year/month` only
  * `ticker/year` hybrid (default)
* Query scripts adapt dynamically to partitioning choice.

---

### b. Version Control & Data Integrity

**Analysis:**

* Full dataset versioning impractical.
* Config + metadata versioning lightweight; track parameters, fetch dates, screening API parameters.
* Hash/checksum tracking ensures integrity.

**Recommendation (Actionable):**

* **Config + metadata versioning** for datasets.
* Track **hashes/checksums** for raw + cleaned data.
* Include **screening API parameters** in metadata to ensure reproducibility of ML subsets.

---

### c. Caching + Refresh Logic

**Analysis:**

* Staging cache for downloads → cleaning → validation → append.
* Daily refresh for trading; weekly for historical backfill.
* Incremental updates preferred; rebuild only on corruption.

**Recommendation (Actionable):**

* **Staging cache** stores recent downloads + hashes.
* Refresh configurable via YAML.
* Incremental updates; append only validated data.
* Stock screening results integrated as **subset cache** to avoid re-querying API every run.

---

## **# Follow-up Questions Analysis & Recommendations**

1. **Pilot subset vs full S&P500 for historical data:**

   * **Full S&P500:** Used for overall analysis and top-K ranking.
   * **Stock Screening API subset:** User-configurable; reduces ML training size.
   * Recommendation: Default → full S&P500 for ranking; optionally filter via screening API for ML subset.

2. **API batching (parallel vs sequential):**

   * Both implemented; configurable in YAML or ArgumentParser.
   * Default sequential, parallel optional for speed with rate-limit awareness.

3. **Staging Cache – Keep old versions vs overwrite:**

   * Keep **hashed snapshots** of recent raw pulls.
   * Overwrite processed dataset once validated. Configurable rolling history (e.g., last N days/weeks).

4. **Corporate Action Adjustments:**

   * Pull **raw first**, adjust post-storage.
   * Keep raw + cleaned for reproducibility and debugging.

---

## **Final Deliverables for Phase 2**

| Deliverable                | Description                                                                                                                 |
| -------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| `src/data/pipeline.py`     | Modular connectors: historical/trading data, Finviz screener integration, corporate action adjustments, staging cache logic |
| `data/raw/`                | Raw CSV/Parquet per ticker/year, hash-validated                                                                             |
| `data/processed/`          | Cleaned + adjusted dataset for ML & EDA                                                                                     |
| `data/screened/`           | Optional subset from stock screener API, cached for reproducibility                                                         |
| `config/data_sources.yaml` | API endpoints, batch/parallel options, provider priority, screening API parameters                                          |
| `config/storage.yaml`      | Partitioning options (ticker/year/hybrid), staging paths, refresh frequency, overwrite policy                               |
| `config/versioning.yaml`   | Metadata versioning parameters, hash/checksum tracking, screening API metadata                                              |
| `docs/data_pipeline.md`    | Flowchart & pipeline steps: batch/backfill, staging cache, screening, refresh, error handling                               |

---

## **Implementation Notes**

* Pipeline supports both full S&P500 and **user-configurable screened subsets** for ML.
* Stock screening integrated as optional step via YAML config (`screening_enabled: true/false`).
* Modular connectors + staging cache + hash validation ensure data integrity and reproducibility.
* Partitioning and batch modes configurable for flexibility and efficiency.

---

