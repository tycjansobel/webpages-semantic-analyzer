from collections import Counter
from logging import Logger
from typing import Literal
import spacy

class FeatureExtractService:
    def __init__(self, logger: Logger) -> None:
        self.nlp = spacy.load('pl_core_news_lg')
        self.logger = logger
        
    def extract_feature_from_text(self, feature: Literal["NOUN"], text: str) -> list[tuple[str, int]]:
        try:        
            doc = self.nlp(text)
            nouns = []
            
            for token in doc:
                if token.pos_ == feature:
                    nouns.append(token.lemma_.lower())
            
            noun_frequencies = Counter(nouns)
            
            return noun_frequencies.most_common()
        
        except Exception as e:
            self.logger.error(f"Error extracting nouns: {e}")
            raise e