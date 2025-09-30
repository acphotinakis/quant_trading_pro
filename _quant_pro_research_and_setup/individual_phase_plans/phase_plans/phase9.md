**Phase 9 – Deployment / Productionization integration plan**

**Objectives & Scope**
The objective of Phase 9 is to move Quant Trading Pro into a production-ready environment where all prior research, validation, and ranking logic can run automatically and consistently. This includes automating daily data refreshes, executing trained models to generate updated stock rankings, and persisting those results into a centralized database (Postgres/Supabase). Additionally, a web-based dashboard will be implemented via Next.js to visualize the latest results in an intuitive, user-friendly format. The scope is focused on operationalizing the system for live use rather than new feature development. Deliverables will include a deployment guide (`docs/phase9_objectives.md`), scheduled jobs, and a functional web interface.

**Universe / Asset Selection**
In this phase, the asset universe remains aligned with prior phases, primarily the S&P 500 (or selected equity universe defined earlier) to ensure continuity and comparability. The emphasis is not on redefining the universe but on ensuring production processes can handle current and future constituents with minimal manual intervention. Historical survivorship bias issues should already be addressed in earlier phases, but live feeds need monitoring to handle ticker changes or corporate actions. Deliverables will include a finalized universe definition file in `data/universe/live_universe.csv`.

**Data Sources & APIs**
The production system will rely on the same data sources vetted in earlier phases, with priority on stable, rate-limit–aware connectors. Primary providers (e.g., Yahoo Finance, Alpha Vantage, or Interactive Brokers) must be paired with backup strategies in case of outages. Rate-limit handling and batching are critical since daily refreshes need to complete within narrow time windows. Deliverables include updated modular data connectors stored in `config/data_sources.yaml` with fallback logic embedded.

**Data Acquisition & Storage**
Daily refresh pipelines will retrieve raw market data and save it in partitioned formats (Parquet/Feather) for traceability, with checksums or hash logs to ensure integrity. Cleaned and feature-ready datasets will be stored separately to reduce latency in model execution. Supabase/Postgres will serve as the central production database for storing daily rankings and metadata, while local or cloud object storage (e.g., S3, GCS) will maintain historical archives. Deliverables will include automated ETL scripts, data partitioning strategies, and schema migrations.

**Feature Engineering / Analysis**
Feature engineering itself will not change significantly in Phase 9, but the priority shifts toward stability and reproducibility. Metrics like liquidity, volatility, and trendiness that powered earlier models must now be recomputed daily in a consistent manner. Monitoring must be added to track potential drift in feature distributions over time, flagging unusual behavior. Deliverables include logs, diagnostic plots, and verification reports in `data/processed/validation_logs/`.

**Infrastructure / Pipeline**
The infrastructure will rely on scheduled jobs (e.g., CRON, Render jobs, or Supabase Edge Functions) that refresh data and run models daily. Pipelines must support incremental updates, caching, and robust error handling with logging for failures. The system should include retry logic, alerting mechanisms, and staging caches to avoid interruptions in production runs. Deliverables include deployment-ready pipeline scripts (`src/data/pipeline.py`) and infrastructure-as-code configs for reproducibility.

**Evaluation / Success Metrics**
Success in Phase 9 is defined by reliable end-to-end automation and accurate, reproducible model outputs. Metrics will focus less on predictive power and more on operational KPIs such as uptime, job completion rates, error frequency, and data latency. Financial evaluation metrics like Sharpe, turnover, or IC can still be monitored daily to ensure ongoing model validity. Deliverables will include a YAML config file for success metrics and dashboards visualizing both operational and financial health.

**Constraints & Assumptions**
Phase 9 assumes access to affordable cloud compute/storage capable of running daily refreshes within a reasonable time window. Retail-level resources should suffice, though scaling options must be documented for future enterprise-level loads. API constraints, including rate limits, will be critical, and handling market data only during regular trading hours (RTH) may simplify implementation. Deliverables will include configuration notes on resource requirements and limitations.

**Version Control / Reproducibility**
All production code, configs, and schemas will be maintained in Git for versioning. Metadata, logs, and job status reports will be preserved for traceability, ensuring results can be reproduced for any given day. While full dataset versioning may be impractical, metadata hashes and Parquet snapshots will ensure reproducibility of rankings. Deliverables include Git-tracked configs, logging systems, and reproducibility checklists.

**Iteration / Next Steps**
Phase 9 connects naturally to long-term scaling, monitoring, and model retraining. Once the production pipeline is stable, the next steps include adding more advanced dashboards, real-time updates, multi-model ensemble support, and integration with brokerage APIs for paper/live trading. This phase establishes the foundation for expanding beyond research and into fully operational trading deployment. Deliverables include backlog notes and next-step roadmaps.
