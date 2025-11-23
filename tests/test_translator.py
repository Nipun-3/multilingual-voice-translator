"""
Unit tests for language translator
"""
import pytest
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from soruce.main import get_language_code, translator_function

def test_get_language_code():
    """Test language code mapping"""
    assert get_language_code("English") == "en"
    assert get_language_code("Tamil") == "ta"
    assert get_language_code("Spanish") == "es"

def test_translator_function():
    """Test translation function"""
    result = translator_function("Hello", "en", "es")
    assert result is not None
    assert hasattr(result, 'text')
    assert len(result.text) > 0

def test_translator_function_spanish():
    """Test Spanish translation"""
    result = translator_function("Hello", "en", "es")
    # Should translate to Spanish
    assert result.dest == "es"

@pytest.mark.skip(reason="Requires internet connection")
def test_integration():
    """Integration test - requires actual API calls"""
    result = translator_function("Hello world", "en", "ta")
    assert result.text is not None

