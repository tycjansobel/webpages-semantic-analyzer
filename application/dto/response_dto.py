from pydantic import BaseModel, HttpUrl
from typing import Dict, Dict

class AnalysisResponseDTO(BaseModel):
    nouns: Dict[HttpUrl, Dict[str, int]]
    similarities: Dict[str, float]