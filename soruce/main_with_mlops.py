"""
Enhanced main.py with MLOps tracking
Integrates MLflow for experiment tracking and monitoring
"""

import os
import time
import pygame
from gtts import gTTS
import streamlit as st
import speech_recognition as sr
from googletrans import LANGUAGES, Translator
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mlflow_tracking import TranslationTracker

isTranslateOn = False

translator = Translator()
pygame.mixer.init()

# Initialize MLflow tracker
tracker = TranslationTracker(experiment_name="language-translator-production")

# Create a mapping between language names and language codes
language_mapping = {name: code for code, name in LANGUAGES.items()}


def get_language_code(language_name):
    return language_mapping.get(language_name, language_name)


def translator_function(spoken_text, from_language, to_language):
    return translator.translate(
        spoken_text, src="{}".format(from_language), dest="{}".format(to_language)
    )


def text_to_voice(text_data, to_language):
    myobj = gTTS(text=text_data, lang="{}".format(to_language), slow=False)
    myobj.save("cache_file.mp3")
    audio = pygame.mixer.Sound("cache_file.mp3")
    audio.play()
    # Wait for audio to finish playing before continuing
    while pygame.mixer.get_busy():
        time.sleep(0.1)
    os.remove("cache_file.mp3")


def main_process(output_placeholder, from_language, to_language):
    # Track session metrics
    session_metrics = {
        "total": 0,
        "successful": 0,
        "failed": 0,
        "total_latency": 0.0,
        "languages": {},
    }

    while isTranslateOn:
        start_time = time.time()
        rec = sr.Recognizer()

        with sr.Microphone() as source:
            output_placeholder.text("Listening...")
            rec.pause_threshold = 1
            audio = rec.listen(source, phrase_time_limit=10)

        try:
            output_placeholder.text("Processing...")
            spoken_text = rec.recognize_google(
                audio, language="{}".format(from_language)
            )

            # Skip if no speech detected
            if not spoken_text or not spoken_text.strip():
                continue

            output_placeholder.text("Translating...")
            translation_start = time.time()
            translated_text = translator_function(
                spoken_text, from_language, to_language
            )
            translation_latency = time.time() - translation_start

            # Calculate total latency
            total_latency = time.time() - start_time

            # Log to MLflow
            tracker.log_translation(
                source_lang=from_language,
                target_lang=to_language,
                source_text=spoken_text,
                translated_text=translated_text.text,
                latency=total_latency,
                success=True,
            )

            # Update session metrics
            session_metrics["total"] += 1
            session_metrics["successful"] += 1
            session_metrics["total_latency"] += total_latency
            lang_pair = f"{from_language}->{to_language}"
            session_metrics["languages"][lang_pair] = (
                session_metrics["languages"].get(lang_pair, 0) + 1
            )

            text_to_voice(translated_text.text, to_language)

        except sr.UnknownValueError:
            # No speech detected
            session_metrics["total"] += 1
            session_metrics["failed"] += 1
            continue
        except Exception as e:
            # Log error to MLflow
            error_latency = time.time() - start_time
            tracker.log_translation(
                source_lang=from_language,
                target_lang=to_language,
                source_text="",
                translated_text="",
                latency=error_latency,
                success=False,
                error=str(e),
            )
            session_metrics["total"] += 1
            session_metrics["failed"] += 1
            print(e)
            continue

    # Log batch metrics at end of session
    if session_metrics["total"] > 0:
        avg_latency = session_metrics["total_latency"] / session_metrics["total"]
        tracker.log_batch_metrics(
            total_translations=session_metrics["total"],
            successful=session_metrics["successful"],
            failed=session_metrics["failed"],
            avg_latency=avg_latency,
            languages_used=session_metrics["languages"],
        )


# UI layout
st.title("Language Translator - MLOps Enabled")

# Sidebar for MLflow metrics
with st.sidebar:
    st.header("📊 MLOps Dashboard")
    st.info("MLflow tracking is active. Check MLflow UI for detailed metrics.")

    if st.button("View MLflow UI"):
        st.write("Run: `mlflow ui` in terminal to view tracking UI")

# Dropdowns for selecting languages
from_language_name = st.selectbox("Select Source Language:", list(LANGUAGES.values()))
to_language_name = st.selectbox("Select Target Language:", list(LANGUAGES.values()))

# Convert language names to language codes
from_language = get_language_code(from_language_name)
to_language = get_language_code(to_language_name)

# Button to trigger translation
start_button = st.button("Start")
stop_button = st.button("Stop")

# Check if "Start" button is clicked
if start_button:
    if not isTranslateOn:
        isTranslateOn = True
        output_placeholder = st.empty()
        main_process(output_placeholder, from_language, to_language)

# Check if "Stop" button is clicked
if stop_button:
    isTranslateOn = False
