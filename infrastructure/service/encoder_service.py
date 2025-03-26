from logging import Logger
from typing import List
from sentence_transformers import SentenceTransformer

MODEL_NAME = 'sdadas/stella-pl'

class EncoderService:
    def __init__(self, logger: Logger) -> None:
        self.model = SentenceTransformer(model_name_or_path=MODEL_NAME, device='cpu', trust_remote_code=True)
        self.logger = logger
    
    def encode(self, text: str) -> List[float]:
        try:
            vector = self.model.encode(sentences=text, normalize_embeddings=True)
            return vector.tolist()
        except Exception as e:
            self.logger.error(f"Cannot encode text {e}")
            raise e
