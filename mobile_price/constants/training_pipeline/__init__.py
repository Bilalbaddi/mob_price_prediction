import os
import numpy as np


'''
training pipeline constants or comman constant
'''
TARGET_COLUMN_NAME = "price_range"
PIPELINE_NAME : str = "MobilePrice"
ARTIFACT_DIR : str = "Artifacts"
FILE_NAME : str = "dataset.csv"
train_file_name : str = 'train.csv'
test_file_name  : str= 'test.csv'
SCHEMA_FILE_PATH = os.path.join("Data_schema", "schema.yaml")

SAVED_MODEL_DIR :str = os.path.join("saved_models")
SAVED_MODEL_NAME : str = "model.pkl"


'''
Data Ingestion Constant
'''

data_ingestion_dir :str= "Data Ingestion"
data_ingestion_database_name :str = "mobile_pricing_data"
data_ingestion_collection_name : str = "pricingdb"
data_ingestion_feature_name : str = "feature_store"
data_ingestion_ingested_name : str = "ingested"
train_test_split_ratio : float = 0.25
 
'''
Data Validation constant 
'''
data_validation_dir_name : str = "Data Validation"
data_validation_validate_dir_name : str = "validate"
data_validation_invalid_dir_name : str = "invalid"
data_validation_report_dir : str = "drift_report"
data_validation_drift_report_name : str = "report.yaml"


'''
Data Transformation
'''
data_transformation_dir_name : str = 'Data Transformation'
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR : str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR : str = "transformed_object"
PREPROCESSING_OBJECT_FILE_NAME :str = "preprocessing.pkl"

