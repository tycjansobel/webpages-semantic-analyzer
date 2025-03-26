from typing import List, Tuple
from pydantic import BaseModel, Field, HttpUrl

class SimilarityModel(BaseModel):
    url: str = Field(default='')
    score: float = Field(default=0)

class AnalysisModel(BaseModel):
    url: str = Field(default='')
    nouns: List[Tuple[str, int]] = Field(default_factory=list)
    vector: List[float] = Field(default_factory=list)
    similarities: List[SimilarityModel] = Field(default_factory=list)