# Quant Trading Pro - Updated Developer-Level Analysis & Implementation Plan

## 1. High-Level Critique (Quant Perspective) - UPDATED

* **Enhanced temporal validation** - Implemented expanding window with 1-year gap between train/test and regime-aware OOS testing using VIX + macroeconomic regime classification
* **Feature stability framework** - Added rolling 6-month feature importance correlation tracking with automated pruning when correlation <0.7
* **Advanced transaction cost modeling** - Expanded beyond Amihud to include bid-ask spread proxies, dynamic slippage scenarios (5/10/20bps), and liquidity-adjusted costs
* **Comprehensive risk management** - Implemented 5% single-stock, 25% sector caps PLUS volatility-adjusted position sizing using 20-day realized volatility
* **Multi-objective model selection** - Clear criteria: IC > 0.02 for development, net Sharpe > 1.0 for production with 3-month rolling validation
* **Sophisticated regime detection** - VIX-based regimes enhanced with Treasury yield curves, market breadth, and economic indicators for robust regime classification
* **Optimized storage strategy** - Store only aggregated daily features, keep raw 5-min data for top-K subset with 30-day rolling window (reduces storage from 3TB to 200GB)
* **Robust backtest validation** - Multiple cost scenarios + corporate action handling + overnight risk modeling
* **Intelligent GPU utilization** - GPU for XGBoost training and large matrix operations, CPU for data loading and preprocessing
* **Comprehensive data quality** - Daily completeness checks (>95% tickers) with automated re-fetch and anomaly detection
* **Adaptive model calibration** - Quarterly retraining with monthly forward validation and drift-based triggers
* **Resilient failure recovery** - Checkpointing with cloud storage sync and intelligent resume capabilities

## 2. Detailed Phase Breakdown (Phases 1 → 10) - UPDATED

### Phase 1 - Research & Scoping
**Objectives**: Define project foundations with enhanced regime awareness
```
Developer Tasks:
- scripts/setup/repo_init.py (Git, folder structure)
- config/success_metrics.yaml (Sharpe, IC, regime-aware thresholds)
- docs/project_objectives.md (goals documentation)
- tests/test_configs.py (YAML validation)
- src/regimes/initial_classification.py (basic regime definitions)

Data & APIs: Macro indicators (VIX, Treasury yields) for regime definition
Compute & Storage: Minimal (2GB), basic file operations + regime data
Failure Modes: Config validation failures, regime data unavailability
Logging: setup.log with timestamp, validation results, regime stats
Deliverables: 
  docs/project_objectives.md
  config/success_metrics.yaml  
  config/system_limits.yaml
  config/regime_definitions.yaml
  data/universe/sp500_constituents.csv
Runtime: 3 hours (includes regime data collection)
```

### Phase 2 - Data Acquisition & Infrastructure
**Objectives**: Build robust data pipeline with enhanced quality monitoring
```
Developer Tasks:
- src/data/pipeline.py (modular API connectors with retry logic)
- config/data_sources.yaml (provider priorities, fallback chains)
- src/data/validation.py (comprehensive data quality checks)
- src/data/regime_data.py (macro indicator collection)
- tests/test_pipeline.py (mock API tests + failure scenarios)

Data & APIs: 
  Primary: Alpaca (5-min OHLCV) + Yahoo (macro data)
  Backup: Interactive Brokers + Alpha Vantage
  Enhanced: VIX, Treasury yields, market breadth indicators
  Backup: Daily S3 snapshots with checksum verification

Compute & Storage:
  Memory: 8GB batch processing with streaming validation
  Storage: 200GB Parquet, partitioned by ticker/year/month/day
  Batch: 50 tickers parallel, adaptive rate limiting based on API responses

Failure Modes: API rate limits, network failures, data corruption
Logging: data_acquisition.log with ticker-level success/failure + quality metrics
Deliverables:
  data/raw/{ticker}/YYYY/MM/DD.parquet
  data/processed/topK_50.csv
  data/regimes/macro_indicators.parquet
  logs/data_pipeline/daily_{date}.log
  reports/data_quality_dashboard.html
Runtime: 4 hours initial, 45min daily updates (includes macro data)
```

### Phase 3 - Exploratory Data Analysis
**Objectives**: Compute and validate features with stability analysis
```
Developer Tasks:
- src/features/eda_pipeline.py (batch feature computation with parallelization)
- config/eda.yaml (rolling windows, stability thresholds)
- src/features/analytics.py (statistical tests + regime analysis)
- src/features/stability.py (feature decay detection)
- tests/test_features.py (feature validation + stability tests)

Data & APIs: Processed OHLCV + macro regime indicators
Compute & Storage:
  Memory: 16GB for full universe processing with Dask parallelization
  Storage: 50GB for feature storage + stability metrics
  Batch: Process by year with checkpointing

Failure Modes: Numerical instability, memory overflow, regime misclassification
Logging: feature_generation.log with compute times, stability metrics, regime correlations
Deliverables:
  data/processed/eda_features.csv
  data/processed/feature_stability_scores.csv
  plots/liquidity_distributions.png
  plots/volatility_regimes.png  
  plots/feature_decay_curves.png
  data/processed/feature_correlations.csv
Runtime: 8 hours initial computation (parallelized)
```

### Phase 4 - Feature Engineering & Selection
**Objectives**: Create ML-ready features with enhanced stability validation
```
Developer Tasks:
- src/features/daily_pipeline.py (daily feature updates with drift detection)
- config/feature_selection.yaml (correlation thresholds, stability requirements)
- src/features/stability.py (rolling correlation + regime stability)
- src/features/interactions.py (cross-sectional ranking features)
- tests/test_stability.py (stability validation + interaction tests)

Data & APIs: EDA features + regime classifications
Compute & Storage:
  Memory: 8GB for daily updates + stability computations
  Storage: 30GB for normalized features + interaction terms
  Processing: Incremental daily updates (8min) with weekly full recomputation

Failure Modes: Feature correlation breakdown, normalization errors, drift detection false positives
Logging: daily_features.log with IC, stability scores, regime performance
Deliverables:
  data/processed/features/normalized/daily_features.parquet
  data/processed/features/interaction_terms.parquet
  data/processed/features/feature_metadata.yaml
  logs/feature_selection/stability_report.csv
  reports/feature_performance_by_regime.md
Runtime: 1.5 hours daily (includes interaction terms)
```

### Phase 5 - Modeling & Signal Development
**Objectives**: Train ranking models with regime-aware validation
```
Developer Tasks:
- src/models/train_pipeline.py (model training with regime stratification)
- config/models.yaml (hyperparameters, regime-specific parameters)
- src/models/evaluation.py (IC, Sharpe, regime performance)
- src/models/validation.py (temporal cross-validation with gaps)
- tests/test_models.py (model validation + regime tests)

Data & APIs: Normalized features + regime labels
Compute & Storage:
  Memory: 16GB for model training with GPU utilization
  Storage: 15GB for model artifacts + regime performance
  GPU: XGBoost training (5x speedup), neural networks if applicable

Failure Modes: Data leakage, overfitting, regime instability, GPU memory issues
Logging: model_training.log with cross-validation scores, regime performance, feature importance
Deliverables:
  models/ranking/xgboost_v1.joblib
  models/performance/training_metrics.csv
  models/performance/regime_analysis.csv
  reports/model_evaluation.md
  src/models/ensemble_weights.py (model blending by regime)
Runtime: 3 hours training (with GPU), 20min daily inference
```

### Phase 6 - Transaction Cost & Execution Modeling
**Objectives**: Incorporate realistic costs with multiple scenarios
```
Developer Tasks:
- src/execution/cost_model.py (Amihud + spread estimation + dynamic slippage)
- config/execution.yaml (cost parameters, multiple scenarios)
- src/execution/position_sizing.py (liquidity-aware + volatility-adjusted sizing)
- src/execution/stress_test.py (extreme market condition simulation)
- tests/test_costs.py (cost validation + stress test scenarios)

Data & APIs: Model signals + OHLCV + liquidity metrics
Compute & Storage:
  Memory: 6GB for cost computation + stress testing
  Storage: 8GB for cost-adjusted signals + scenario analysis
  Processing: Daily batch with weekly stress testing

Failure Modes: Extreme liquidity events, missing bid-ask data, stress test convergence
Logging: execution_costs.log with cost distribution, scenario analysis, sizing adjustments
Deliverables:
  data/processed/execution/cost_adjusted_signals.parquet
  data/processed/execution/liquidity_buckets.csv
  data/processed/execution/stress_test_results.parquet
  reports/cost_analysis.md
  reports/position_sizing_validation.md
Runtime: 45 minutes daily (includes basic stress testing)
```

### Phase 7 - Backtesting Framework
**Objectives**: Simulate strategy with comprehensive risk constraints
```
Developer Tasks:
- src/backtesting/engine.py (portfolio simulation with corporate actions)
- config/backtest.yaml (constraint parameters, leverage limits)
- src/backtesting/analysis.py (performance metrics + risk analysis)
- src/backtesting/risk_management.py (overnight risk, drawdown controls)
- tests/test_backtest.py (backtest validation + corporate action tests)

Data & APIs: Cost-adjusted signals + universe data + corporate actions
Compute & Storage:
  Memory: 12GB for full history backtest with risk calculations
  Storage: 20GB for backtest results + risk metrics
  Processing: Parallel by year with checkpointing

Failure Modes: Look-ahead bias, corporate action mishandling, risk limit violations
Logging: backtest.log with constraint violations, performance, risk metrics
Deliverables:
  data/backtests/daily_portfolios.parquet
  data/backtests/risk_metrics.csv
  reports/backtest_performance.md
  reports/corporate_action_handling.md
  plots/equity_curve.png
  plots/drawdown_analysis.png
Runtime: 2 hours for full history, 8min for walk-forward (parallelized)
```

### Phase 8 - Validation & Robustness Checks
**Objectives**: Rigorous OOS testing with enhanced regime analysis
```
Developer Tasks:
- src/validation/walk_forward.py (expanding window tests with regime stratification)
- config/validation.yaml (robustness thresholds, regime requirements)
- src/validation/regime_analysis.py (comprehensive market regime tests)
- src/validation/sensitivity.py (parameter sensitivity analysis)
- tests/test_validation.py (validation checks + regime stability)

Data & APIs: Backtest results + benchmark data + enhanced regime indicators
Compute & Storage:
  Memory: 12GB for multiple test scenarios + regime analysis
  Storage: 15GB for validation artifacts + sensitivity results
  Processing: Overnight batch processing with parallel regime analysis

Failure Modes: Regime misclassification, insufficient OOS data, sensitivity test overload
Logging: validation.log with fold-level performance, regime stats, sensitivity outcomes
Deliverables:
  reports/validation_report.md
  data/validation/walk_forward_results.parquet
  data/validation/regime_performance.parquet
  plots/regime_performance.png
  plots/sensitivity_analysis.png
  reports/parameter_stability.md
Runtime: 5 hours for comprehensive validation (parallelized)
```

### Phase 9 - Deployment / Productionization
**Objectives**: Automate daily pipeline with enhanced monitoring
```
Developer Tasks:
- scripts/deployment/daily_pipeline.py (orchestration with checkpointing)
- config/deployment.yaml (schedule, alerts, retry logic)
- src/monitoring/health_checks.py (comprehensive system monitoring)
- src/monitoring/alert_system.py (email/Slack notifications)
- tests/test_deployment.py (integration tests + failure recovery tests)

Data & APIs: Live market data feeds + model inference
Compute & Storage:
  Memory: 10GB for daily runs + monitoring overhead
  Storage: Cloud database (Supabase) + local cache for redundancy
  Processing: Scheduled 1hr after market close with retry logic

Failure Modes: API outages, data corruption, model inference failures, storage full
Logging: deployment.log with pipeline status, errors, recovery actions, performance metrics
Deliverables:
  Live database with daily rankings + regime tags
  Web dashboard (Next.js) with performance analytics
  monitoring/alert_history.json
  reports/daily_pipeline_status.html
  scripts/recovery/auto_resume.py
Runtime: 60 minutes daily automated (with retry buffer)
```

### Phase 10 - Monitoring & Iteration
**Objectives**: Continuous improvement with advanced drift detection
```
Developer Tasks:
- src/monitoring/drift_detection.py (feature/model monitoring with adaptive thresholds)
- config/monitoring.yaml (alert thresholds, retraining triggers)
- src/research/expansion.py (new universe research with regime analysis)
- src/monitoring/performance_attribution.py (return decomposition)
- tests/test_monitoring.py (monitoring validation + synthetic drift tests)

Data & APIs: Production results + expanded data sources + alternative data
Compute & Storage:
  Memory: 6GB for monitoring tasks + research computations
  Storage: 25GB for historical monitoring data + research results
  Processing: Daily monitoring + weekly research + monthly expansion analysis

Failure Modes: Silent model degradation, monitoring false positives, research overfitting
Logging: monitoring.log with drift scores, retraining triggers, research outcomes
Deliverables:
  reports/monitoring_dashboard.md
  data/monitoring/feature_drift.csv
  data/monitoring/model_performance_trends.csv
  research/expansion_backtests/
  reports/adaptive_retraining_framework.md
Runtime: 45 minutes daily monitoring, 6 hours weekly research
```

## 3. Software Engineering Blueprint - UPDATED

### Enhanced Repo Layout
```
quant_trading_pro/
├── config/                          # YAML configuration files
│   ├── data_sources.yaml           # API endpoints, rate limits, fallback chains
│   ├── models.yaml                 # Hyperparameters, regime-specific models
│   ├── execution.yaml              # Cost models, multiple scenarios
│   ├── regime_definitions.yaml     # VIX, macro indicators, thresholds
│   └── system_limits.yaml          # Resource constraints, alert thresholds
├── data/
│   ├── raw/                        # Original API data
│   │   └── {ticker}/YYYY/MM/DD.parquet
│   ├── processed/                  # Cleaned and feature data
│   │   ├── features/
│   │   ├── universe/
│   │   ├── regimes/                # Regime classifications
│   │   └── execution/
│   ├── backtests/                  # Portfolio simulations
│   ├── validation/                 # OOS testing results
│   └── models/                     # Trained model artifacts
├── src/
│   ├── data/                       # Data acquisition and validation
│   ├── features/                   # Feature engineering + stability
│   ├── models/                     # ML training + regime validation
│   ├── execution/                  # Cost modeling + stress testing
│   ├── backtesting/                # Portfolio simulation + risk management
│   ├── validation/                 # Robustness testing + sensitivity
│   ├── monitoring/                 # Production monitoring + drift detection
│   ├── regimes/                    # Regime detection + classification
│   └── utils/                      # Shared utilities + parallel processing
├── scripts/
│   ├── deployment/                 # Production orchestration + recovery
│   ├── analysis/                   # One-off analysis + research
│   ├── monitoring/                 # Monitoring and alerting
│   └── setup/                      # Environment setup
├── tests/
│   ├── unit/                       # Module-level tests
│   ├── integration/                # Pipeline integration tests
│   ├── performance/                # Memory and runtime profiling
│   └── fixtures/                   # Test data + synthetic scenarios
├── logs/                           # Structured application logs
├── plots/                          # Generated analysis visualizations
├── reports/                        # Automated reporting
└── docs/                           # Project documentation + diagrams
```

### Enhanced Config Strategy
```yaml
# config/system_limits.yaml
compute:
  max_memory_gb: 32
  max_cores: 8
  use_gpu: true
  gpu_memory_gb: 8
  max_runtime_hours: 6
  parallel_workers: 4

storage:
  max_disk_gb: 1000
  parquet_compression: zstd
  retention_days:
    raw: 60
    processed: 180
    models: 90
    backtests: 365

api:
  rate_limit_per_minute: 100
  max_retries: 5
  timeout_seconds: 30
  fallback_chain: ["alpaca", "yfinance", "ibkr"]

# config/models.yaml
models:
  baseline:
    - name: "logistic_regression"
      class: "sklearn.linear_model.LogisticRegression"
      params:
        C: 1.0
        max_iter: 1000
        
  production_candidates:
    - name: "xgboost_ranking"
      class: "xgboost.XGBRanker"
      params:
        n_estimators: 200
        max_depth: 6
        learning_rate: 0.1
        tree_method: "gpu_hist"  # GPU acceleration
        
training:
  temporal_validation:
    train_size: 0.7
    val_size: 0.2
    test_size: 0.1
    gap_days: 252
    expanding_window: true
    
  regime_validation:
    vix_thresholds: [15, 30]
    macro_regimes: ["expansion", "contraction"]
    require_regime_stability: true
    
  evaluation:
    primary_metric: "information_coefficient"
    secondary_metric: "sharpe_ratio"
    min_ic: 0.02
    min_sharpe: 1.0
    max_drawdown: 0.15
    regime_consistency: 0.7

# config/execution.yaml
transaction_costs:
  base_scenario: 0.0010  # 10bps
  optimistic_scenario: 0.0005  # 5bps
  pessimistic_scenario: 0.0020  # 20bps
  liquidity_adjusted: true
  
position_sizing:
  single_stock_cap: 0.05
  sector_cap: 0.25
  volatility_adjusted: true
  max_portfolio_vol: 0.15
  overnight_risk_limit: 0.02

stress_testing:
  liquidity_shocks: true
  volatility_spikes: true
  correlation_breakdown: true
  frequency: "weekly"
```

### Enhanced Data Storage & Partitioning
- **Format**: Parquet with Zstd compression (better compression than Snappy)
- **Partitioning**: 
  - Raw: `ticker/year/month/day` for efficient time-range queries
  - Features: `feature_type/date` with regime tags
  - Backtests: `strategy/regime/date` for organized analysis
- **Metadata**: Enhanced `metadata.json` with hash, creation time, data schema, regime context
- **Retention**: 60 days raw, 6 months processed, 3 months model artifacts, 1 year backtests
- **Backup**: Critical files to cloud storage with versioning
- **Optimization**: Only store raw 5-min data for top-K subset, aggregate others to daily

### Enhanced Pipeline Staging
```
ingestion/     -> src/data/pipeline.py (with quality checks)
cleaning/      -> src/data/validation.py (with anomaly detection)
regime/        -> src/regimes/classification.py (parallel processing)
feature/       -> src/features/daily_pipeline.py (with stability monitoring)
train/         -> src/models/train_pipeline.py (with regime stratification)
predict/       -> src/models/inference.py (with confidence intervals)
execution/     -> src/execution/cost_model.py (multiple scenarios)
backtest/      -> src/backtesting/engine.py (with risk management)
validation/    -> src/validation/walk_forward.py (regime-aware)
deploy/        -> scripts/deployment/daily_pipeline.py (with checkpointing)
monitor/       -> src/monitoring/drift_detection.py (adaptive thresholds)
```

### Enhanced Testing Strategy
- **Unit tests**: Mock APIs, validate data transformations, regime classification
- **Integration tests**: Full pipeline runs on sample data with synthetic regimes
- **Performance tests**: Memory and runtime profiling on large datasets with parallelization
- **Failure recovery tests**: Simulate API failures, data corruption, recovery scenarios
- **Regime stability tests**: Validate model performance across different market conditions
- **Stress tests**: Extreme market scenario validation

### Enhanced Orchestration & Monitoring
- **Scheduling**: GitHub Actions with matrix strategies for parallel backtests
- **Experiment tracking**: MLflow + custom regime metadata tracking
- **Dependency management**: Poetry with environment-specific locks
- **Containerization**: Docker with GPU support for reproducible training
- **Monitoring**: Prometheus metrics + Grafana dashboards for pipeline health
- **Alerting**: Multi-channel (email, Slack) with escalating severity

### Enhanced Security & Cost Controls
- **API keys**: HashiCorp Vault or AWS Secrets Manager for production
- **Cost monitoring**: Real-time API spend tracking with automatic throttling
- **Cloud spend**: Multi-tier budgets with $50/month soft limit, $100/month hard limit
- **Data encryption**: AES-256 at rest, TLS in transit, key rotation quarterly
- **Access control**: RBAC for different pipeline stages and data sensitivity

## 4. Refined Next Steps (Priority Action Plan) - UPDATED

1. **Setup enhanced project infrastructure** (Effort: S)
   - Initialize Git repo with new folder structure
   - Create configuration templates with regime-aware defaults
   - Acceptance: All config files validate, regime data collection works

2. **Implement data acquisition with quality monitoring** (Effort: M)  
   - Build Alpaca connector with adaptive rate limiting
   - Create enhanced data validation with anomaly detection
   - Acceptance: Download 1 month of data with >98% quality score

3. **Develop regime detection framework** (Effort: M)
   - Implement VIX + macro regime classification
   - Create regime-aware data partitioning
   - Acceptance: Regimes correctly identify 2008, 2020 market periods

4. **Build feature computation with stability tracking** (Effort: L)
   - Implement features with parallel computation
   - Add stability monitoring and decay detection
   - Acceptance: Features computed with stability scores >0.7

5. **Create regime-aware model training** (Effort: M)
   - Implement XGBoost with GPU acceleration
   - Add regime-stratified cross-validation
   - Acceptance: IC > 0.02 across all major regimes

6. **Develop advanced transaction cost model** (Effort: M)
   - Implement multiple cost scenarios + stress testing
   - Create volatility-adjusted position sizing
   - Acceptance: Costs show realistic liquidity dependence

7. **Build comprehensive backtesting engine** (Effort: L)
   - Implement with corporate action handling
   - Add risk management and drawdown controls
   - Acceptance: No violations of risk limits in historical tests

8. **Create enhanced validation framework** (Effort: M)
   - Implement walk-forward testing with regime tags
   - Add parameter sensitivity analysis
   - Acceptance: OOS performance within 15% of IS across regimes

9. **Setup production with monitoring** (Effort: M)
   - Create daily pipeline with checkpointing
   - Implement comprehensive alert system
   - Acceptance: Pipeline recovers automatically from simulated failures

10. **Develop advanced drift detection** (Effort: M)
    - Implement adaptive monitoring thresholds
    - Create automated retraining triggers
    - Acceptance: Detects synthetic drift within 5 days

11. **Optimize performance and scalability** (Effort: M)
    - Profile and optimize memory usage across phases
    - Implement intelligent parallelization
    - Acceptance: Daily pipeline runs <45 minutes with 8 cores

12. **Document and package for deployment** (Effort: S)
    - Create comprehensive deployment guide
    - Package with Docker and cloud configuration
    - Acceptance: New user can setup and run in <90 minutes

## Enhanced Questions / Decisions to Surface

1. **Regime detection sophistication**
   - Options: VIX-only, VIX+macro, ML-based regime clustering
   - Recommendation: VIX + Treasury yield curve + market breadth
   - Impact: Phases 2, 3, 5, 8

2. **Feature stability monitoring frequency**
   - Options: Daily, Weekly, Monthly, On-drift
   - Recommendation: Weekly full analysis + daily spot checks
   - Impact: Phases 3, 4, 10

3. **GPU utilization strategy**
   - Options: CPU-only, GPU for training, GPU for training+inference
   - Recommendation: GPU for XGBoost + neural networks, CPU for data processing
   - Impact: Phases 4, 5, 9

4. **Stress testing comprehensiveness**
   - Options: Basic liquidity, Full historical, Synthetic scenarios
   - Recommendation: Historical crises + synthetic tail events
   - Impact: Phases 6, 7, 8

5. **Model ensemble strategy**
   - Options: Single model, Equal weighting, Regime-based weighting, ML meta-learner
   - Recommendation: Regime-based weighting initially, ML meta-learner later
   - Impact: Phase 5, 9, 10

6. **Data quality tolerance thresholds**
   - Options: 90%, 95%, 98% completeness requirements
   - Recommendation: 95% for daily operations, 98% for model training
   - Impact: Phases 2, 9

7. **Backtest calibration frequency**
   - Options: Never, Quarterly, Annually, On regime change
   - Recommendation: Quarterly + on major regime changes
   - Impact: Phases 7, 8, 10

8. **Monitoring alert escalation**
   - Options: Email only, Email+Slack, Automated phone, Multi-level escalation
   - Recommendation: Email+Slack with 2-level escalation for critical alerts
   - Impact: Phase 9, 10

9. **Cloud deployment strategy**
   - Options: Fully local, Hybrid, Fully cloud, Multi-cloud
   - Recommendation: Hybrid - local processing with cloud backup and monitoring
   - Impact: Phases 9, 10

10. **Research expansion priority**
    - Options: More equities, International, Alternative data, New asset classes
    - Recommendation: Alternative data first, then international equities
    - Impact: Phase 10

11. **Model interpretability requirements**
    - Options: Black box, Feature importance only, Full SHAP analysis, Counterfactuals
    - Recommendation: Feature importance + regime-specific SHAP
    - Impact: Phases 5, 8, 10

12. **Risk limit enforcement**
    - Options: Hard stops, Soft limits with alerts, Dynamic based on volatility
    - Recommendation: Hard stops for position limits, dynamic for volatility
    - Impact: Phases 6, 7, 9

13. **Cost scenario selection for production**
    - Options: Always use base, Worst-case, Regime-adjusted, Dynamic
    - Recommendation: Regime-adjusted with pessimistic bias
    - Impact: Phases 6, 9

14. **Data versioning granularity**
    - Options: Daily snapshots, Weekly, On model change, On regime change
    - Recommendation: Daily for raw data, on model/regime change for features
    - Impact: All phases

15. **Performance attribution depth**
    - Options: Basic, Factor exposure, Regime contribution, Feature contribution
    - Recommendation: Factor + regime attribution initially
    - Impact: Phases 8, 10

16. **Disaster recovery readiness**
    - Options: Manual recovery, Semi-automated, Fully automated with hot standby
    - Recommendation: Semi-automated with documented recovery procedures
    - Impact: Phases 9, 10

This updated plan maintains retail compute constraints while incorporating professional quant rigor through enhanced regime awareness, comprehensive risk management, and robust monitoring systems. The parallel processing and intelligent storage strategies ensure scalability within typical retail hardware limitations.