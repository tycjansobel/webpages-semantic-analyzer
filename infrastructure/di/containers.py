from logging import Logger
from dependency_injector import containers, providers

from application.service.analysis_service import AnalysisService
from infrastructure.service.encoder_service import EncoderService
from infrastructure.service.feature_extract_service import FeatureExtractService
from infrastructure.service.scrape_service import ScrapeService

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["api.endpoints"])
    
    logger = providers.Singleton(Logger, name="")

    encoder_service = providers.Singleton(EncoderService, logger=logger)
    
    feature_extract_service = providers.Singleton(FeatureExtractService, logger=logger)
    
    scrape_service = providers.Singleton(ScrapeService, logger=logger)
    
    analysis_service = providers.Factory(
        AnalysisService,
        encoder_service = encoder_service,
        feature_extract_service = feature_extract_service,
        scrape_service = scrape_service,
        logger = logger
    )