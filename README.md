# Real-Time Language Translator Bot

## 01 Introduction

A voice recognition-based tool for translating languages in real-time. This tool serves as a virtual interpreter, offering users a convenient and efficient way to bridge language gaps. Inspired by the natural process of human translation, the tool listens to spoken words and converts them into the target language, replicating the fluidity and accuracy of a human translator.

 ![Banner Image](docs/media/0-banner-image.png)

 ## 02 Technology Stack

 - Python (v3.8.5 Recommended)
 - GTTS Module
 - SpeechRecognition Module
 - Streamlit UI Module 
 - Pygame Module
 - Googletrans (v3.1.0a0 Recommended)

 ## 03 System Architeture Diagram

 ![diagram](docs/media/1-system-architeture.png)

## 04 Setup

- **Step 01:** Navigate to the following directory.

  ```
   language-translator-bot/docs/requirements.txt
  ```

- **Step 02:** Run this command to install all dependencies.

  ```
   pip install -r requirements.txt
  ```



## 05 Usage

### Basic Usage

- **Step 01:** Navigate to the source directory.

  ```
   language-translator-bot/soruce/main.py
  ```

- **Step 02:** Run this command to launch the app.

  ```
   streamlit run main.py
  ```

### MLOps-Enabled Version

For experiment tracking and monitoring:

```bash
# Quick start with MLOps
chmod +x start_mlops.sh
./start_mlops.sh

# Or manually:
pip install -r requirements-mlops.txt
mlflow ui &
streamlit run soruce/main_with_mlops.py
```

View MLflow dashboard at: `http://localhost:5001` (Note: Port 5000 is used by macOS AirPlay)

## 06 MLOps Features

This project includes a complete free MLOps pipeline:

- ✅ **MLflow Tracking**: Experiment tracking and metrics logging
- ✅ **CI/CD Pipeline**: Automated testing and deployment via GitHub Actions
- ✅ **Performance Monitoring**: Latency, success rate, and usage analytics
- ✅ **Automated Testing**: Unit tests and code quality checks
- ✅ **Deployment Ready**: Streamlit Cloud and Hugging Face Spaces compatible

See [MLOPS_SETUP.md](MLOPS_SETUP.md) for detailed setup instructions.
