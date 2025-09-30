#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status

echo "Creating project directory..."

echo "Creating folder structure..."
mkdir -p config/
mkdir -p data/{universe,regimes,raw,processed,backtests,validation,models}
mkdir -p src/{data,features,models,execution,backtesting,validation,monitoring,regimes,utils}
mkdir -p scripts/{setup,deployment,analysis,monitoring}
mkdir -p tests/{unit,integration,performance,fixtures}
mkdir -p logs/
mkdir -p plots/
mkdir -p reports/
mkdir -p docs/

echo "Project structure created successfully!"
