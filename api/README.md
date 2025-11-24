# Flask API for Language Translator

Minimal REST API for language translation.

## Quick Start

```bash
cd api
pip install -r requirements.txt
python app.py
```

API will run on: `http://localhost:5000`

## Endpoints

### 1. Health Check
```
GET /
```
Returns API status

### 2. Translate Text
```
POST /translate
Content-Type: application/json

{
    "text": "Hello, how are you?",
    "from_lang": "English",
    "to_lang": "Spanish"
}
```

Response:
```json
{
    "original_text": "Hello, how are you?",
    "translated_text": "Hola, ¿cómo estás?",
    "source_language": "en",
    "target_language": "es"
}
```

### 3. Get Languages
```
GET /languages
```
Returns list of all supported languages

### 4. Generate Audio
```
POST /audio
Content-Type: application/json

{
    "text": "Hola, ¿cómo estás?",
    "language": "Spanish"
}
```

Returns base64-encoded MP3 audio

## Example Usage

```python
import requests

# Translate
response = requests.post("http://localhost:5000/translate", json={
    "text": "Hello world",
    "from_lang": "English",
    "to_lang": "French"
})
print(response.json())
```

