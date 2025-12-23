# Quant Trading Pro - Phase 6 Checklist

This checklist covers the tasks for Phase 6: Transaction Cost & Execution Modeling. The goal is to build realistic models for trading costs (slippage, commissions) and to develop execution-aware rules for position sizing, transforming raw model signals into practical, cost-adjusted signals.

---

### 1. Setup & Configuration

- [ ] **Create Execution Modeling Module:**
    - [ ] Create a new module at `src/execution/cost_model.py` to house functions for slippage and transaction cost estimation.
- [ ] **Create Position Sizing Module:**
    - [ ] Create `src/execution/position_sizing.py` for rules on liquidity-aware position sizing.
- [ ] **Create Execution Configuration File:**
    - [ ] Create `config/execution.yaml` to define parameters for cost models (e.g., slippage coefficients), liquidity buckets, and position sizing rules (e.g., ADV caps).
- [ ] **Create Test File:**
    - [ ] Create `tests/unit/test_execution.py` to unit test the cost and position sizing calculations.

### 2. Transaction Cost Modeling

- [ ] **Implement Slippage Model:**
    - [ ] In `cost_model.py`, implement an Amihud-based slippage model that estimates price impact based on trade size and a stock's illiquidity.
    - [ ] Add logic to simulate multiple cost scenarios (e.g., optimistic, base, pessimistic) based on different assumptions.
- [ ] **Implement Commission Model:**
    - [ ] Add a function to model broker commissions based on a configurable schedule (e.g., per-share or percentage of value).
- [ ] **Create Liquidity Buckets:**
    - [ ] Develop a function to group stocks into liquidity quintiles or deciles based on their average dollar volume or Amihud score.
    - [ ] Analyze and report average costs per bucket.

### 3. Position Sizing & Signal Adjustment

- [ ] **Implement Liquidity-Aware Position Sizing:**
    - [ ] In `position_sizing.py`, create rules to cap position sizes based on a stock's Average Daily Volume (ADV), e.g., not exceeding 10% of ADV.
- [ ] **Signal Adjustment:**
    - [ ] Create a pipeline that takes raw model scores from Phase 5 and adjusts them based on estimated transaction costs, penalizing signals for illiquid stocks.

### 4. Infrastructure & Pipeline

- [ ] **Create Execution Pipeline Script:**
    - [ ] Develop a script `src/execution/execution_pipeline.py` that orchestrates the application of cost models and position sizing rules to the raw signals.
    - [ ] The pipeline should output a set of cost-adjusted, sized signals ready for backtesting.
- [ ] **Logging:**
    - [ ] Add logging to `logs/execution/` to track estimated costs, position size adjustments, and any tickers excluded due to extreme illiquidity.

### 5. Deliverables & Documentation

- [ ] **Cost-Adjusted Signals:**
    - [ ] Save the final, cost-adjusted signals to `data/processed/execution/cost_adjusted_signals.parquet`.
- [ ] **Analysis Reports:**
    - [ ] Generate and save reports on cost distributions per liquidity bucket to `reports/cost_analysis.md`.
    - [ ] Generate plots comparing pre- and post-cost signal distributions.
- [ ] **Unit Tests:**
    - [ ] Implement tests in `tests/unit/test_execution.py` to validate the slippage calculations and position sizing logic.
- [ ] **Documentation:**
    - [ ] Create the handoff document `docs/phase6_to_phase7.md`, explaining the cost models and position sizing rules that need to be integrated into the backtesting engine.
    - [ ] Ensure all new functions have clear docstrings.
