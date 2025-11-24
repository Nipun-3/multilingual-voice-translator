"""
Minimal FastAPI for Language Translator
Provides REST API endpoint for translation
"""
from fastapi import FastAPI, HTTPException
from googletrans import LANGUAGES, Translator

app = FastAPI(
    title="Language Translator API",
    description="Minimal FastAPI for text translation",
    version="1.0.0"
)

translator = Translator()

# Create language mapping
language_mapping = {name: code for code, name in LANGUAGES.items()}


def get_language_code(language_name: str) -> str:
    """Convert language name to code"""
    return language_mapping.get(language_name, language_name)


@app.get("/")
def health_check():
    """Health check endpoint"""
    return {"status": "ok", "message": "Language Translator API"}


@app.post("/translate")
def translate_text(request: dict):
    """
    Translate text from one language to another
    
    - **text**: The text to translate (required)
    - **from_lang**: Source language name (default: "English")
    - **to_lang**: Target language name (default: "Spanish")
    """
    try:
        text = request.get("text")
        from_lang = request.get("from_lang", "English")
        to_lang = request.get("to_lang", "Spanish")
        
        if not text:
            raise HTTPException(status_code=400, detail="Text is required")
        
        # Convert language names to codes
        from_code = get_language_code(from_lang)
        to_code = get_language_code(to_lang)
        
        # Translate
        result = translator.translate(text, src=from_code, dest=to_code)
        
        return {
            "original_text": text,
            "translated_text": result.text,
            "source_language": from_code,
            "target_language": to_code,
            "confidence": getattr(result, 'confidence', None)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5011)

