"""
MLflow Tracking for Language Translator
Tracks translation metrics, latency, and usage statistics
"""
import mlflow
import mlflow.sklearn
from datetime import datetime
import time
from typing import Dict, Optional

class TranslationTracker:
    """Track translation experiments and metrics"""
    
    def __init__(self, experiment_name: str = "language-translator"):
        """Initialize MLflow tracking"""
        mlflow.set_experiment(experiment_name)
        self.experiment_name = experiment_name
    
    def log_translation(
        self,
        source_lang: str,
        target_lang: str,
        source_text: str,
        translated_text: str,
        latency: float,
        success: bool = True,
        error: Optional[str] = None
    ):
        """Log a single translation event"""
        with mlflow.start_run(run_name=f"translation_{datetime.now().strftime('%Y%m%d_%H%M%S')}"):
            # Log parameters
            mlflow.log_param("source_language", source_lang)
            mlflow.log_param("target_language", target_lang)
            
            # Log metrics
            mlflow.log_metric("latency_ms", latency * 1000)  # Convert to milliseconds
            mlflow.log_metric("success", 1 if success else 0)
            mlflow.log_metric("text_length", len(source_text))
            
            # Log metadata
            mlflow.log_dict({
                "source_text": source_text[:100],  # First 100 chars
                "translated_text": translated_text[:100],
                "timestamp": datetime.now().isoformat(),
                "error": error if error else None
            }, "translation_metadata.json")
    
    def log_batch_metrics(
        self,
        total_translations: int,
        successful: int,
        failed: int,
        avg_latency: float,
        languages_used: Dict[str, int]
    ):
        """Log batch statistics"""
        with mlflow.start_run(run_name=f"batch_stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}"):
            mlflow.log_metric("total_translations", total_translations)
            mlflow.log_metric("successful", successful)
            mlflow.log_metric("failed", failed)
            mlflow.log_metric("success_rate", successful / total_translations if total_translations > 0 else 0)
            mlflow.log_metric("avg_latency_ms", avg_latency * 1000)
            mlflow.log_dict(languages_used, "language_usage.json")

