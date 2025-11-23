"""
Web-compatible version for Streamlit Cloud
Uses text input instead of microphone (works in browser)
"""
import streamlit as st
from googletrans import LANGUAGES, Translator
from gtts import gTTS
import base64
import os

translator = Translator()

# Create a mapping between language names and language codes
language_mapping = {name: code for code, name in LANGUAGES.items()}


def get_language_code(language_name):
    return language_mapping.get(language_name, language_name)


def translator_function(spoken_text, from_language, to_language):
    return translator.translate(spoken_text, src='{}'.format(from_language), dest='{}'.format(to_language))


def text_to_audio_bytes(text_data, to_language):
    """Generate audio and return as bytes for browser playback"""
    tts = gTTS(text=text_data, lang='{}'.format(to_language), slow=False)
    audio_file = "temp_audio.mp3"
    tts.save(audio_file)
    
    with open(audio_file, "rb") as f:
        audio_bytes = f.read()
    
    os.remove(audio_file)
    return audio_bytes


# UI layout
st.title("Language Translator - Web Version")

st.info("🌐 Web-compatible version: Enter text instead of using microphone")

# Dropdowns for selecting languages
from_language_name = st.selectbox("Select Source Language:", list(LANGUAGES.values()))
to_language_name = st.selectbox("Select Target Language:", list(LANGUAGES.values()))

# Convert language names to language codes
from_language = get_language_code(from_language_name)
to_language = get_language_code(to_language_name)

# Text input instead of microphone
user_text = st.text_input("Enter text to translate:", placeholder="Type your text here...")

# Button to trigger translation
translate_button = st.button("Translate")

if translate_button and user_text:
    try:
        with st.spinner("Translating..."):
            # Translate
            translated_text = translator_function(user_text, from_language, to_language)
            
            # Display translation
            st.success("Translation:")
            st.write(f"**{translated_text.text}**")
            
            # Generate and play audio
            with st.spinner("Generating audio..."):
                audio_bytes = text_to_audio_bytes(translated_text.text, to_language)
                st.audio(audio_bytes, format="audio/mp3")
                
    except Exception as e:
        st.error(f"Error: {str(e)}")

