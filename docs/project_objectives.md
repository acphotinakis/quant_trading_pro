# Quant Trading Pro - Project Objectives

## Primary Goal
Develop a systematic, machine learning-driven stock trading system that can:
1. **Rank U.S. equities daily** based on liquidity, volatility, and trendiness
2. **Select a top-K subset of stocks** for algorithmic trading and ML modeling  
3. **Predict short-term price movements** and directional trends
4. **Integrate risk and transaction cost considerations** for realistic trading

## Core Objectives

### Stock Ranking & Selection
- Identify promising stocks daily using cross-sectional metrics
- Maintain top-K subset (50 stocks) based on volume, liquidity, and trendiness
- Ensure selection process is reproducible and backtestable

### Machine Learning Pipeline
- Build features from intraday 5-min OHLCV data
- Train models for relative ranking and absolute direction prediction
- Validate predictive power through Information Coefficient (IC > 0.02)
- Incorporate feature stability and transaction costs

### Infrastructure & Data Pipeline
- Maintain robust data acquisition from multiple providers
- Implement efficient storage (Parquet) with version control
- Support incremental updates and data validation
- Ensure reproducibility across all phases

### Risk Management
- Define capital allocation constraints ($25k-$100k retail capital)
- Implement position sizing (5% single-stock, 25% sector caps)
- Model transaction costs (5-20bps scenarios)
- Include drawdown controls and regime-aware risk

## Success Criteria

### Operational Success
- Full 5-min dataset ingested and cleaned (>95% completeness)
- Top-K subset consistently updated and stored
- Data pipelines produce reproducible outputs with logs
- Daily pipeline runs completed within 45 minutes

### Analytical Success  
- EDA produces stable, interpretable features (stability > 0.7)
- Features validated for cross-sectional and rolling-window stability
- Models show positive predictive power (IC > 0.02)
- Performance consistent across market regimes

### Trading Success
- Simulated backtests show Sharpe ratio > 1.2 (net of costs)
- Maximum drawdown < 25% in stress testing
- Turnover < 10% monthly
- Hit rate > 52% consistently

## Constraints & Assumptions

### Retail Compute Constraints
- Single workstation: 8-16 cores, 32-64GB RAM, optional GPU
- Storage: 1TB NVMe SSD maximum
- Network: Standard broadband, no colocation
- Budget: Limited cloud spending ($50-100/month)

### Data Assumptions
- Universe: S&P 500 current constituents initially
- Data: 5-min OHLCV, RTH only initially
- History: 10+ years where available
- Providers: Alpaca primary, Yahoo/IB backup

### Trading Assumptions  
- Capital: $25,000 - $100,000 retail allocation
- Costs: 5-20bps transaction costs
- No leverage initially
- Long-only positions initially

