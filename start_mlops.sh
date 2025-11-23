#!/bin/bash

# Quick start script for MLOps-enabled Language Translator

echo "🚀 Starting MLOps Pipeline for Language Translator..."

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements-mlops.txt

# Start MLflow UI in background
echo "📊 Starting MLflow UI..."
mlflow ui --port 5001 --host 127.0.0.1 &
MLFLOW_PID=$!

# Wait a moment for MLflow to start
sleep 3

echo "✅ MLflow UI running at http://localhost:5001"
echo "🌐 Starting Streamlit app..."
echo ""

# Start Streamlit app
streamlit run soruce/main_with_mlops.py

# Cleanup on exit
trap "kill $MLFLOW_PID 2>/dev/null" EXIT

