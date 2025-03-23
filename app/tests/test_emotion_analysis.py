import pytest
from unittest.mock import patch
from services.emotion_analysis import analyze_emotion, extract_keywords
import services.emotion_analysis as emotion_analysis

@pytest.mark.asyncio
async def test_analyze_emotion():
    """Test the analyze_emotion function with mock pipeline response."""
    test_input = "I am feeling very happy today!"
    
    # Mocking the emotion analysis pipeline output
    mock_result = [{"label": "joy"}]
    with patch("services.emotion_analysis.emotion_analyzer", return_value=mock_result):
        result = await analyze_emotion(test_input)
        assert result == "joy"

@pytest.mark.asyncio
async def test_extract_keywords():
    """Test the extract_keywords function with mock KeyBERT output."""
    test_input = "Machine learning and artificial intelligence are revolutionizing industries."
    
    # Mocking the KeyBERT output
    mock_keywords = [("machine learning", 0.9), ("artificial intelligence", 0.85), ("industries", 0.8)]
    with patch.object(emotion_analysis.kw_model, "extract_keywords", return_value=mock_keywords):
        result = await extract_keywords(test_input)
        assert result == ["machine learning", "artificial intelligence", "industries"]

@pytest.mark.asyncio
async def test_extract_keywords_with_long_text():
    """Test extract_keywords function with long text exceeding 500 characters."""
    test_input = " ".join(["word"] * 150)  # Generate a long text (150 words)
    
    mock_keywords = [("long text", 0.9), ("word repetition", 0.85)]
    with patch.object(emotion_analysis.kw_model, "extract_keywords", return_value=mock_keywords):
        result = await extract_keywords(test_input)
        assert result == ["long text", "word repetition"]
