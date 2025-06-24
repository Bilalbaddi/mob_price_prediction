import os
from mobile_price.constants import training_pipeline
from mobile_price.exception.exception import PricingException
from mobile_price.logging.logger import logging
import pandas as pd
import numpy as np
from datetime import datetime


class TRAININGPIPELINECONFIG:
    def __init__(self,timestamp = datetime.now()):
        timestamp = timestamp.strftime("%m-%d-%Y-%H-%M-%S")
        self.pipeline_name = training_pipeline.PIPELINE_NAME
        self.artifact_name = training_pipeline.ARTIFACT_DIR
        self.artifact_dir = os.path.join(self.artifact_name, timestamp)
        self.timestamp : str = timestamp


class DataIngestionConfig:
    def __init__(self,training_pipeline_config : TRAININGPIPELINECONFIG):
        self.data_ingestion_dir : str = os.path.join(training_pipeline_config.artifact_dir,training_pipeline.data_ingestion_dir)
        self.feature_file_path : str = os.path.join(self.data_ingestion_dir,training_pipeline.data_ingestion_feature_name,training_pipeline.FILE_NAME)
        self.train_file_path : str = os.path.join(self.data_ingestion_dir,training_pipeline.data_ingestion_ingested_name,training_pipeline.train_file_name)
        self.test_file_path : str = os.path.join(self.data_ingestion_dir,training_pipeline.data_ingestion_ingested_name,training_pipeline.test_file_name)
        self.collection_name : str = training_pipeline.data_ingestion_collection_name
        self.database : str = training_pipeline.data_ingestion_database_name
        self.train_test_split_ratio : float = training_pipeline.train_test_split_ratio
class DataValidationConfig:
    def __init__(self,training_pipeline_config: TRAININGPIPELINECONFIG):
        self.data_validation_dir_path : str = os.path.join(training_pipeline_config.artifact_dir,training_pipeline.data_validation_dir_name)
        self.data_validation_valid_dir_pth : str = os.path.join(self.data_validation_dir_path,training_pipeline.data_validation_validate_dir_name)
        self.invalid_data_dir : str = os.path.join(self.data_validation_dir_path, training_pipeline.data_validation_invalid_dir_name)
        self.valid_train_file_path : str = os.path.join(self.data_validation_valid_dir_pth, training_pipeline.train_file_name)
        self.valid_test_file_path : str = os.path.join(self.data_validation_valid_dir_pth, training_pipeline.test_file_name)
        self.invalid_train_file_path : str = os.path.join(self.invalid_data_dir, training_pipeline.train_file_name)
        self.invalid_test_file_path : str = os.path.join(self.invalid_data_dir, training_pipeline.test_file_name)
        self.drift_report_file_path : str = os.path.join(self.data_validation_dir_path, training_pipeline.data_validation_report_dir,training_pipeline.data_validation_drift_report_name)

class DataTransformationConfig:
    def __init__(self,training_pipeline_config:TRAININGPIPELINECONFIG):
        self.data_transformatiom_dir : str = os.path.join(training_pipeline_config.artifact_dir,training_pipeline.data_transformation_dir_name)
        self.train_transformed_file_path : str = os.path.join(self.data_transformatiom_dir,training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
                                                        training_pipeline.train_file_name.replace("csv","npy"))
        self.test_transformed_file_path : str = os.path.join(self.data_transformatiom_dir,training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
                                                       training_pipeline.test_file_name.replace("csv","npy"))
        self.transformed_object_file_path : str = os.path.join(self.data_transformatiom_dir,training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,
                                                               training_pipeline.PREPROCESSING_OBJECT_FILE_NAME)


class ModelTrainerConfig:
    def __init__(self,training_pipeline_config:TRAININGPIPELINECONFIG):
        self.model_trainer_dir_name : str = os.path.join(training_pipeline_config.artifact_dir,training_pipeline.MODEL_TRAINER_DIR_NAME)
        self.trained_model_file_path : str = os.path.join(self.model_trainer_dir_name,training_pipeline.MODEL_TRAINER_TRAINED_MODEL_DIR,
                                                          training_pipeline.MODEL_TRAINER_TRAINED_MODEL_NAME)
        self.expected_accuracy : float = training_pipeline.MODEL_TRAINER_EXPECTED_SCORE
        self.overfotting_underfitting_threshold : float =  training_pipeline.MODEL_TRAINER_OVERFITTING_UNDERFITTING_THRESHOLD
        
        