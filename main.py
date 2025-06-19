from mobile_price.logging.logger import logging
from mobile_price.entity.config_entity import  DataIngestionConfig,TRAININGPIPELINECONFIG
from mobile_price.components.data_ingestion import DataIngestion
# from mobile_price.components.data_validation import DataValidation
# from mobile_price.components.model_trainer import ModelTrainer
# from mobile_price.components.data_transformation import DataTransformation
from mobile_price.exception.exception import PricingException

import sys
from mobile_price.constants import training_pipeline


if __name__ == "__main__":
    try:
        trainingpipelineconfig = TRAININGPIPELINECONFIG()
        dataingestionconfig = DataIngestionConfig(trainingpipelineconfig)
        dataingestion = DataIngestion(dataingestionconfig)
        logging.info("Starting data ingestion process")
        dataingestionartifacts = dataingestion.initiate_data_ingestion()
        logging.info("Data ingestion process completed successfully")
        print(dataingestionartifacts)
    except Exception as e:
        raise PricingException(e,sys) from e