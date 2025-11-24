"""
Minimal Flask API for Language Translator
Provides REST API endpoints for translation
"""
from flask import Flask, request, jsonify
from flasgger import Swagger
from googletrans import LANGUAGES, Translator
from gtts import gTTS
import base64
import io
import os

app = Flask(__name__)
swagger = Swagger(app)
translator = Translator()

# Create language mapping
language_mapping = {name: code for code, name in LANGUAGES.items()}


def get_language_code(language_name):
    """Convert language name to code"""
    return language_mapping.get(language_name, language_name)


@app.route("/", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "ok", "message": "Language Translator API"})


@app.route("/translate", methods=["POST"])
def translate_text():
    """
    Translate text from one language to another
    ---
    tags:
      - Translation
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - text
          properties:
            text:
              type: string
              example: "Hello, how are you?"
            from_lang:
              type: string
              example: "English"
            to_lang:
              type: string
              example: "Spanish"
    responses:
      200:
        description: Translation successful
      400:
        description: Bad request
      500:
        description: Server error
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        text = data.get("text")
        from_lang = data.get("from_lang", "English")
        to_lang = data.get("to_lang", "Spanish")
        
        if not text:
            return jsonify({"error": "Text is required"}), 400
        
        # Convert language names to codes
        from_code = get_language_code(from_lang)
        to_code = get_language_code(to_lang)
        
        # Translate
        result = translator.translate(text, src=from_code, dest=to_code)
        
        return jsonify({
            "original_text": text,
            "translated_text": result.text,
            "source_language": from_code,
            "target_language": to_code,
            "confidence": getattr(result, 'confidence', None)
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/languages", methods=["GET"])
def get_languages():
    """
    Get list of supported languages
    ---
    tags:
      - Languages
    responses:
      200:
        description: List of supported languages
    """
    return jsonify({
        "languages": dict(LANGUAGES),
        "total": len(LANGUAGES)
    }), 200


@app.route("/audio", methods=["POST"])
def generate_audio():
    """
    Generate audio from translated text
    ---
    tags:
      - Audio
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - text
          properties:
            text:
              type: string
              example: "Hola, ¿cómo estás?"
            language:
              type: string
              example: "Spanish"
    responses:
      200:
        description: Audio generated successfully
      400:
        description: Bad request
      500:
        description: Server error
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        text = data.get("text")
        language = data.get("language", "Spanish")
        
        if not text:
            return jsonify({"error": "Text is required"}), 400
        
        # Convert language name to code
        lang_code = get_language_code(language)
        
        # Generate audio
        tts = gTTS(text=text, lang=lang_code, slow=False)
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        
        # Convert to base64 for JSON response
        audio_base64 = base64.b64encode(audio_buffer.read()).decode('utf-8')
        
        return jsonify({
            "audio_base64": audio_base64,
            "format": "mp3",
            "language": lang_code
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5010)

