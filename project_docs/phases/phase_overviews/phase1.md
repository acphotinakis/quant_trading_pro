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

---

### **Infrastructure / Pipeline**

Phase 1 sets up project infrastructure for reproducibility and future automation. This includes initializing a Git repository with `/docs`, `/config`, and `/data/universe` folders, preparing `docs/project_timeline.md` for the overall phase plan, and optionally integrating task management tools (Trello, Notion, GitHub issues). Deliverables include the structured repo, timeline document, and any initial issue templates. Considerations include deciding the granularity of task tracking, integration with later data pipelines, and documentation standards to maintain cross-phase consistency.

---

### **Constraints & Assumptions**

Phase 1 is bounded by **retail compute and storage constraints**, requiring careful planning for dataset size, API usage, and runtime expectations. Assumptions include focusing on current S&P 500 constituents, using intraday 5-min data where feasible, and deferring extended-hours or external datasets to later phases. Deliverables include the documented assumptions in `docs/constraints.md`. Considerations involve ensuring these constraints are communicated clearly to avoid infeasible requests in Phase 2 and Phase 3.

---

### **Version Control / Reproducibility**

All project artifacts (docs, configs, and universe lists) are version-controlled via Git. Reproducibility is reinforced by storing system limits and success metrics in structured YAML files, ensuring that subsequent phases can reliably reference initial assumptions. Deliverables include a Git repo with `/docs`, `/config`, `/data/universe`, and logs if needed. Considerations include tracking any changes to the universe or metrics that could affect downstream reproducibility.

---

### **Iteration / Next Steps**

Phase 1 outputs feed directly into **Phase 2 – Data Acquisition & Infrastructure**, providing the universe definitions, selected data providers, and system constraints that shape pipeline design. Key next steps include finalizing top-K candidate selection criteria, referencing success metrics in Phase 2 pipeline configs, and verifying storage and runtime plans against retail compute resources. Deliverables include a documented handoff in `docs/phase1_to_phase2.md`. Considerations include clarifying any uncertainties in universe composition, data provider priority, and constraints before Phase 2 begins.
