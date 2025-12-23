# Quant Trading Pro - Phase 4 Checklist

This checklist outlines the necessary tasks to complete Phase 4: Feature Engineering & Selection. The goal is to build a stable, daily, ML-ready feature set from the EDA features and select the most predictive and robust candidates for modeling.

---

### 1. Setup & Configuration

- [ ] **Create Feature Pipeline Script:**
    - [ ] Create the main pipeline script at `src/features/daily_pipeline.py` to automate daily feature generation, normalization, and selection.
- [ ] **Create Feature Selection Configuration:**
    - [ ] Create `config/feature_selection.yaml` to store parameters for stability analysis, correlation thresholds, and IC requirements.
- [ ] **Create Test File:**
    - [ ] Create `tests/unit/test_stability.py` to house unit tests for feature stability and selection logic.

### 2. Feature Pipeline Development

- [ ] **Implement Daily Feature Aggregation:**
    - [ ] In `daily_pipeline.py`, build a function to load the EDA features from `data/processed/eda_features.parquet`.
    - [ ] Create logic to compute any new interaction or lagged features.
- [ ] **Implement Normalization:**
    - [ ] Implement a function for robust cross-sectional normalization (e.g., rank-based) as the default.
    - [ ] Add an optional z-score normalization for comparison.
- [ ] **Implement Rolling Stability Analysis:**
    - [ ] Create a function to calculate the rolling correlation of feature ranks over time (e.g., 6-month rolling window) to measure stability.
    - [ ] The function should flag or prune features where the stability drops below a configurable threshold (e.g., < 0.7).

### 3. Feature Selection & Pruning

- [ ] **Implement Correlation Pruning:**
    - [ ] Develop a function to compute the correlation matrix of the feature set.
    - [ ] Automatically identify and prune highly correlated features (e.g., correlation > 0.9), keeping the one with higher stability.
- [ ] **Implement Predictive Power Analysis (Information Coefficient):**
    - [ ] Create a function to compute the Information Coefficient (IC) of each feature against a forward-return target.
    - [ ] Analyze IC across different market regimes defined in Phase 1.
- [ ] **Final Feature Selection:**
    - [ ] Combine stability, correlation, and IC analysis to select the final feature set.
    - [ ] Document the rationale for including or excluding features in `docs/feature_selection_notes.md`.

### 4. Infrastructure & Automation

- [ ] **Build out `daily_pipeline.py`:**
    - [ ] The script should run end-to-end: load data, generate features, normalize, run stability and correlation checks, and save the final set.
    - [ ] Implement efficient, incremental daily updates.
    - [ ] Add logging to `logs/feature_selection/` to track daily runs, pruned features, and stability scores.

### 5. Deliverables & Documentation

- [ ] **Final Daily Feature Set:**
    - [ ] Save the raw, normalized, and final selected feature sets to `data/processed/features/`.
    - [ ] Store metadata about the feature set (e.g., normalization method, windows) in `data/processed/features/feature_metadata.yaml`.
- [ ] **Unit Tests:**
    - [ ] Implement unit tests in `tests/unit/test_stability.py` for stability calculations and pruning logic.
- [ ] **Documentation:**
    - [ ] Create the handoff document `docs/phase4_to_phase5.md`, summarizing the final feature set and its characteristics for the modeling phase.
    - [ ] Ensure all new functions have clear docstrings.
