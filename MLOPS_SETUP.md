# MLOps Setup Guide

Complete guide to set up free end-to-end MLOps for the Language Translator app.

## 🎯 What's Included

- **MLflow**: Experiment tracking and model registry
- **GitHub Actions**: CI/CD pipeline
- **Monitoring**: Performance metrics and logging
- **Deployment**: Streamlit Cloud / Hugging Face Spaces ready

## 📦 Installation

### 1. Install MLOps Dependencies

```bash
pip install -r requirements-mlops.txt
```

### 2. Set Up MLflow

```bash
# Start MLflow UI (runs on http://localhost:5001)
mlflow ui --config-file mlflow_config.yaml

# Or use default settings
mlflow ui
```

### 3. Run App with MLOps

```bash
# Option 1: Use enhanced version with MLflow tracking
streamlit run soruce/main_with_mlops.py

# Option 2: Use original version
streamlit run soruce/main.py
```

## 🔄 CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/mlops-pipeline.yml`) automatically:

1. **Tests**: Runs linting, formatting checks, and unit tests
2. **Deploys**: Automatically deploys to Streamlit Cloud on push to main

### Setup GitHub Actions

1. Push code to GitHub
2. Actions will run automatically on push/PR
3. Check Actions tab in GitHub for status

## 📊 Monitoring

### View MLflow Dashboard

1. Start MLflow UI: `mlflow ui`
2. Open browser: `http://localhost:5001`
3. View:
   - Translation metrics (latency, success rate)
   - Language pair usage
   - Error tracking
   - Performance trends

### Metrics Tracked

- **Latency**: Translation time in milliseconds
- **Success Rate**: Percentage of successful translations
- **Language Usage**: Frequency of language pairs
- **Error Logs**: Failed translation attempts

## 🚀 Deployment Options

### Option 1: Streamlit Cloud (Free)

1. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
2. Connect your GitHub repo
3. Deploy automatically

### Option 2: Hugging Face Spaces (Free)

1. Create new Space on [huggingface.co/spaces](https://huggingface.co/spaces)
2. Select Streamlit SDK
3. Connect GitHub repo
4. Auto-deploys on push

### Option 3: Local MLflow Server

```bash
# Start MLflow tracking server
mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns

# Set MLflow tracking URI
export MLFLOW_TRACKING_URI=http://localhost:5001
```

## 📈 Usage Analytics

The enhanced app tracks:
- Translation requests per session
- Average latency
- Language pair popularity
- Error rates

View in MLflow UI or export data for analysis.

## 🔧 Configuration

### MLflow Settings

Edit `mlflow_config.yaml` to customize:
- Backend store (SQLite, PostgreSQL, etc.)
- Artifact storage location
- Server host/port

### Streamlit Settings

Edit `.streamlit/config.toml` for:
- Theme customization
- Server configuration
- Browser settings

## 🧪 Testing

Run tests:

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest tests/ -v

# With coverage
pytest tests/ -v --cov=soruce --cov-report=html
```

## 📝 Best Practices

1. **Version Control**: All code changes tracked in Git
2. **Experiment Tracking**: Every translation logged to MLflow
3. **Automated Testing**: CI/CD runs tests on every push
4. **Monitoring**: Real-time metrics in MLflow dashboard
5. **Documentation**: Code documented and maintained

## 🆘 Troubleshooting

### MLflow not starting
```bash
# Check if port 5001 is available (5000 is used by macOS AirPlay)
lsof -i :5001

# Use different port (if 5001 is also taken)
mlflow ui --port 5002
```

### GitHub Actions failing
- Check Actions tab for error logs
- Ensure all dependencies in requirements-mlops.txt
- Verify Python version compatibility

### Import errors
```bash
# Ensure you're in project root
cd /path/to/real-time-language-translator-main

# Install dependencies
pip install -r requirements-mlops.txt
```

## 🎓 Next Steps

1. **Add Custom Models**: Integrate custom translation models
2. **A/B Testing**: Compare different translation APIs
3. **Alerting**: Set up alerts for high error rates
4. **Data Pipeline**: Add data preprocessing pipeline
5. **Model Serving**: Deploy models via MLflow serving

## 📚 Resources

- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Streamlit Cloud](https://docs.streamlit.io/streamlit-community-cloud)
- [Hugging Face Spaces](https://huggingface.co/docs/hub/spaces)

