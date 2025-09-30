#!/bin/bash

# Create directory structure
mkdir -p config data/{raw,processed,features,models} notebooks src/{data,features,models,trading,utils,api} scripts tests docker

# Create configuration files
touch config/config.yaml config/stocks.yaml config/api_keys.yaml

# Create source code files
touch src/__init__.py
touch src/data/__init__.py src/data/data_loader.py src/data/data_preprocessor.py src/data/api_clients.py
touch src/features/__init__.py src/features/technical_indicators.py src/features/fourier_wavelet.py src/features/cross_asset.py src/features/regime_detection.py src/features/gnn_features.py
touch src/models/__init__.py src/models/base_model.py src/models/lstm_forecaster.py src/models/stock_ranker.py src/models/ensemble.py src/models/model_registry.py src/models/transformer_mlp_ensemble.py src/models/rl_portfolio.py
touch src/trading/__init__.py src/trading/trading_engine.py src/trading/portfolio_manager.py src/trading/risk_manager.py src/trading/execution.py
touch src/utils/__init__.py src/utils/config.py src/utils/logger.py src/utils/metrics.py src/utils/helpers.py
touch src/api/__init__.py src/api/app.py

# Create scripts
touch scripts/train.py scripts/predict.py scripts/trading_loop.py scripts/backtest.py scripts/deploy.py

# Create test files
touch tests/__init__.py tests/test_models.py tests/test_trading.py

# Create Docker files
touch docker/Dockerfile docker/docker-compose.yml

# Create project files
touch requirements.txt environment.yml Makefile README.md

# Create notebooks
touch notebooks/01_eda.ipynb notebooks/02_feature_engineering.ipynb notebooks/03_model_experiments.ipynb notebooks/04_backtesting.ipynb

# Create empty __init__.py files for Python packages
find . -type d -name "__pycache__" -prune -o -type f -name "*.py" -print | while read file; do
    dir=$(dirname "$file")
    touch "$dir/__init__.py"
done

echo "Project structure created successfully!"
echo "Total files created: $(find . -type f | wc -l)"