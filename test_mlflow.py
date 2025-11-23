"""
Quick test script to create sample MLflow data
This will populate the dashboard so you can see it working
"""
import mlflow
from mlflow_tracking import TranslationTracker
import time

print("Creating test MLflow experiment...")
print("This will add sample data to the dashboard\n")

# Initialize tracker
tracker = TranslationTracker(experiment_name="language-translator")

# Create some test translations
test_cases = [
    ("en", "es", "Hello, how are you?", "Hola, ¿cómo estás?", 0.5),
    ("en", "fr", "Good morning", "Bonjour", 0.3),
    ("en", "de", "Thank you", "Danke", 0.2),
    ("es", "en", "Buenos días", "Good morning", 0.4),
    ("fr", "en", "Merci beaucoup", "Thank you very much", 0.35),
]

print("Logging test translations...")
for source_lang, target_lang, source_text, translated_text, latency in test_cases:
    tracker.log_translation(
        source_lang=source_lang,
        target_lang=target_lang,
        source_text=source_text,
        translated_text=translated_text,
        latency=latency,
        success=True
    )
    print(f"✓ Logged: {source_lang} → {target_lang}")

# Log batch metrics
tracker.log_batch_metrics(
    total_translations=5,
    successful=5,
    failed=0,
    avg_latency=0.35,
    languages_used={"en->es": 1, "en->fr": 1, "en->de": 1, "es->en": 1, "fr->en": 1}
)

print("\n✅ Test data created!")
print("\nNow start MLflow UI:")
print("  mlflow ui --port 5001")
print("\nThen open: http://localhost:5001")
print("You should see the 'language-translator' experiment with 6 runs!")

