from logging import Logger
from typing import List
from application.dto.request_dto import AnalysisRequestDTO
from application.dto.response_dto import AnalysisResponseDTO
from application.model.analysis_model import AnalysisModel, SimilarityModel
from infrastructure.service.encoder_service import EncoderService
from infrastructure.service.feature_extract_service import FeatureExtractService
from infrastructure.service.scrape_service import ScrapeService
from sentence_transformers import util
    
class AnalysisService:
    def __init__(self, encoder_service: EncoderService, scrape_service: ScrapeService, feature_extract_service: FeatureExtractService, logger: Logger) -> None:
        self.encoder_service = encoder_service
        self.scrape_service = scrape_service
        self.feature_extract_service = feature_extract_service
        self.logger = logger
    
    def analyze(self, dto: AnalysisRequestDTO) -> AnalysisResponseDTO:
        urls = dto.urls
        texts: List[str] = []
        models: List[AnalysisModel] = []
        
        for url in urls:
            text = self.scrape_service.extract_text_from_url(url)
            texts.append(text)

        for url, text in zip(urls, texts):
            model = AnalysisModel()
            model.vector = self.encoder_service.encode(text=text)
            model.nouns = self.feature_extract_service.extract_feature_from_text(feature="NOUN", text=text)
            model.url = url
            models.append(model)
            
        for i in range(len(models)):
            similarities = []
            models_to_compare = [model for model in models if model.url != models[i].url]    
            scores = util.cos_sim(a=[models[i].vector], b=[model.vector for model in models_to_compare])
            
            [scores_list] = scores.tolist()
            
            for score, model in zip(scores_list, models_to_compare):                
                similarities.append(SimilarityModel(url=str(model.url), score=score))
            
            sorted_similarities = sorted(similarities, key = lambda k: k.score, reverse=True)
            models[i].similarities = sorted_similarities

        return self._map_response(models)

    def _map_response(self, models: List[AnalysisModel]) -> AnalysisResponseDTO:
        nouns_dict = {
            str(model.url): {noun: freq for noun, freq in model.nouns}
            for model in models
        }
            
        similarities_dict = {}
        processed_pairs = set()
        
        for model in models:
            for similarity in model.similarities:
                url1 = str(model.url)
                url2 = str(similarity.url)
                url_pair = tuple(sorted([url1, url2]))
                
                if url_pair not in processed_pairs:
                    key = f"{url_pair[0]} vs {url_pair[1]}"
                    similarities_dict[key] = round(float(similarity.score), 2)
                    processed_pairs.add(url_pair)
        
        similarities_dict = dict(
            sorted(
            similarities_dict.items(), 
            key=lambda item: item[1], 
            reverse=True
            )
        )
        
        return AnalysisResponseDTO(
            nouns=nouns_dict,
            similarities=similarities_dict
        )