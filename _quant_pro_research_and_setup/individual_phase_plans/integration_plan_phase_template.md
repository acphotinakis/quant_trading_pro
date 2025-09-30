# **Quant Trading Pro – Phase Criteria Template**

This template can be applied to any phase for clarity, traceability, and reproducibility.

| Category                              | Description                                                           | Deliverables / Examples                         | Considerations / Questions                                                          |
| ------------------------------------- | --------------------------------------------------------------------- | ----------------------------------------------- | ----------------------------------------------------------------------------------- |
| **Objectives & Scope**                | Define what this phase accomplishes and its measurable goals          | Markdown doc (`docs/phaseX_objectives.md`)      | Are we building infrastructure, performing analysis, or creating ML features?       |
| **Universe / Asset Selection**        | Identify the universe of assets or instruments relevant to this phase | CSV lists, notes (`data/universe/...`)          | Current vs historical constituents, ETFs vs equities, survivorship bias             |
| **Data Sources & APIs**               | List APIs, providers, and primary/backup strategies                   | YAML config (`config/data_sources.yaml`)        | Include rate limits, batching, modular connectors                                   |
| **Data Acquisition & Storage**        | How data will be retrieved, stored, partitioned, and versioned        | Parquet/Feather files, hash/checksum logs       | Partitioning by ticker/year, raw vs cleaned, batch vs on-demand backfill            |
| **Feature Engineering / Analysis**    | EDA, normalization, rolling windows, metrics                          | Plots, tables, CSVs (`data/processed/`)         | Liquidity, volatility, trendiness metrics; rolling vs cross-sectional normalization |
| **Infrastructure / Pipeline**         | Compute/storage setup, modularity, caching, refresh logic             | Scripts (`src/data/pipeline.py`), staging cache | Refresh frequency, incremental updates, error handling, logging                     |
| **Evaluation / Success Metrics**      | How success is defined in this phase                                  | YAML config, risk matrix                        | Sharpe, turnover, drawdown, IC, predictive power                                    |
| **Constraints & Assumptions**         | Limits for compute, capital, API usage, storage                       | Docs & config                                   | Retail compute vs enterprise, RTH vs extended-hours, max data history               |
| **Version Control / Reproducibility** | Metadata, hash tracking, logs, config versioning                      | Git repo, logs folder                           | Config + metadata versioning vs full dataset, traceability for ML experiments       |
| **Iteration / Next Steps**            | How this phase connects to the next                                   | Docs, backlog                                   | Identify unresolved questions, potential refinements                                |

---