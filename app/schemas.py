from pydantic import BaseModel, constr
from typing import Dict, Any, Optional

class TextRequest(BaseModel):
      text: constr(min_length=1, max_length=1000) # type: ignore

class MusicRecommendationResponse(BaseModel):
      youtube: list[Dict[str, Any]]