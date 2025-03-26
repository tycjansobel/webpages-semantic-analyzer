from typing import List
from pydantic import BaseModel, Field, HttpUrl

class AnalysisRequestDTO(BaseModel):
    urls: List[HttpUrl] = Field(..., min_length=1, max_length=10)