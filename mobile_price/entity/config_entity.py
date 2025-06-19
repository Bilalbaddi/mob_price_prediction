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
        