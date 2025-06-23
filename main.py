from mobile_price.logging.logger import logging
from mobile_price.entity.config_entity import  DataIngestionConfig,TRAININGPIPELINECONFIG,DataValidationConfig,DataTransformationConfig
from mobile_price.components.data_ingestion import DataIngestion
from mobile_price.components.data_validation import DataValidation
# from mobile_price.components.model_trainer import ModelTrainer
from mobile_price.components.data_transformation import DataTransformation
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



        data_validation_config = DataValidationConfig(trainingpipelineconfig)
        data_validation = DataValidation(data_validation_config=  data_validation_config, data_ingestiion_artifact=  dataingestionartifacts)
        logging.info("Starting data validation process")
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info("Data validation process completed successfully")
        print(data_validation_artifact)


        logging.info("Starting data transformation process")
        data_transformation_config = DataTransformationConfig(trainingpipelineconfig)
        data_transformation = DataTransformation(data_validation_artifact=data_validation_artifact, data_transformation_config=data_transformation_config)
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        logging.info("Data transformation process completed successfully")
    except Exception as e:
        raise PricingException(e,sys) from e