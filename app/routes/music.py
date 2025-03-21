import asyncio, json, logging

from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas import TextRequest, MusicRecommendationResponse
from app.services.emotion_analysis import analyze_emotion, extract_keywords
from app.services.youtube_api import youtube_search

# Create a FastAPI router instance
router = APIRouter()

# Configure logger
logger = logging.getLogger(__name__)

@router.post(
    "/analyze-emotion",
    response_model=MusicRecommendationResponse,
    summary="Emotion-based music recommendation",
    description="Analyzes user input text to extract emotions and keywords, then recommends related music."
)
async def music_recommendation(
   user_input: TextRequest
):
      # Validate user input
      if not user_input.text.strip():
            raise HTTPException(
                  status_code=status.HTTP_400_BAD_REQUEST,
                  detail="Input text is empty."
                  )
    
      logger.info(f"User input: {user_input.text}")

      # Perform asynchronous emotion analysis and keyword extraction concurrently
      try:
            emotion, keywords = await asyncio.gather(
            analyze_emotion(user_input.text),
            extract_keywords(user_input.text)
            )
      except Exception as e:
            logger.error(f"Emotion analysis or keyword extraction failed: {str(e)}")
            raise HTTPException(status_code=500, detail="Error processing text input.")


      # Construct a search query for music recommendations
      search_query = f"{emotion} {' '.join(keywords)} music"
      logger.info(f"Search query: {search_query}")

      # Fetch YouTube videos based on the generated query
      try:
            youtube_videos = await youtube_search(search_query)
      except Exception as e:
            logger.error(f"YouTube search failed: {str(e)}")
            raise HTTPException(status_code=500, detail="Error fetching music recommendations.")
      
      # Prepare the response
      result = {"youtube": youtube_videos}

      return result