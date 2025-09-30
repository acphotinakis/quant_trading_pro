# **Enhanced Prompt – Phase 6 Plan Generator**

**Prompt:**

> You are provided with the **[MASTER INTEGRATION PLAN]**, which documents Phases 1 through 5 of the Quant Trading Pro project. Ingest and understand this context, including objectives, deliverables, dependencies, and cross-phase integration.
>
> Using that knowledge, generate a structured **Phase 6 Integration Plan – Transaction Cost & Execution Modeling** following the **[PHASE TEMPLATE SCHEMA]**.
>
> The **[PHASE INPUT]** for Phase 6 is:
>
> * Implement Amihud-based slippage model.
> * Estimate costs across liquidity buckets.
> * Build position sizing rules (avoid illiquid names).
> * Simulate realistic fill assumptions.
>
> ### Requirements:
>
> 1. For each schema category (Objectives & Scope, Universe/Asset Selection, Data Sources & APIs, Data Acquisition & Storage, Feature Engineering/Analysis, Infrastructure/Pipeline, Evaluation/Success Metrics, Constraints/Assumptions, Version Control/Reproducibility, Iteration/Next Steps), provide:
>
> * **Description** of the activity.
>
> * **Deliverables / Examples** (e.g., scripts, CSVs, YAML configs, Markdown docs, plots, backtest logs).
>
> * **Considerations / Questions** (highlighting where decisions are needed, e.g., “Should slippage be modeled per-ticker or cross-sectionally by bucket?”).
>
> 2. Ensure the plan clearly shows **cross-phase integration**:
>
> * Inputs: Phase 5 model outputs (daily scores & rankings).
>
> * Outputs: Cost-adjusted signals, execution-ready orders, and realistic PnL streams → feeding into Phase 7 (backtesting & portfolio evaluation).
>
> 3. Include **practical reproducibility measures** (config versioning, experiment logs, metadata hashes, simulation assumptions documented).
>
> 4. If any requirements are ambiguous or depend on user preference (e.g., number of liquidity buckets, fill-rate assumptions, position sizing rules), ask **concise clarifying questions** before finalizing that section.
>
> 5. Output in **Markdown format**, suitable for direct saving as `docs/phase6_integration.md`. Include tables where helpful, example config paths, and integration notes.



[PHASE TEMPLATE SCHEMA]

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
[PHASE INPUT]

Phase 6 – Transaction Cost & Execution Modeling
* Implement Amihud-based slippage model.
* Estimate costs across liquidity buckets.
* Build position sizing rules (avoid illiquid names).
* Simulate realistic fill assumptions.


[MASTER INTEGRATION PLAN]

