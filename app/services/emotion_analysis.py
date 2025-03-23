import asyncio
import logging

from transformers import pipeline
from keybert import KeyBERT
from sentence_transformers import SentenceTransformer

# Load emotion analysis model
emotion_analyzer = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")

# Load KeyBERT model for keyword extraction
kw_model = KeyBERT(SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2"))

logger = logging.getLogger(__name__)

async def analyze_emotion(user_input: str):
    """Asynchronous function to analyze the emotion of a given text."""
    try:
        loop = asyncio.get_running_loop()
        # Run the emotion analysis model in a separate thread to prevent blocking
        result = await loop.run_in_executor(None, emotion_analyzer, user_input)
        label = result[0]["label"]
        logger.info(f"[Emotion analyze] input: {user_input} -> result: {label}")
        return label
    except Exception as e:
        logger.error(f"[Error Emotion analyze] input: {user_input} -> error: {e}")
        return "An error occurred"

async def extract_keywords(text: str):
    """Asynchronous function to extract keywords from a given text."""
    try:
        # Trim the text to 500 characters, ensuring words are not cut off
        if len(text) > 500:
            text = text[:500].rsplit(" ", 1)[0]  # Prevents breaking words in the middle
        
        loop = asyncio.get_running_loop()
        # Run the keyword extraction in a separate thread
        keywords = await loop.run_in_executor(
            None,
            lambda: kw_model.extract_keywords(
                text,
                keyphrase_ngram_range=(1, 2),  # Extract both unigrams and bigrams
                stop_words="english",  # Remove common English stopwords
                top_n=3,  # Return the top 3 keywords
                use_mmr=True,  # Enable Maximal Marginal Relevance (MMR) for diversity
                diversity=0.7  # Adjust diversity level (higher = more diverse)
            )
        )
        keyword_list = [kw[0] for kw in keywords]
        logger.info(f"[Extract keywords] input: {text} -> keyword: {keyword_list}")
        return keyword_list
    except Exception as e:
        logger.error(f"[Error Extract keywords] input: {text} -> error: {e}")
        return []
