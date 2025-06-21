from mobile_price.entity.artifact_entity import DataValidationArtifact
from mobile_price.entity.artifact_entity import DataIngestionArtifact
from mobile_price.exception.exception import PricingException
from mobile_price.logging.logger import logging
from mobile_price.entity.config_entity import DataValidationConfig
from mobile_price.constants.training_pipeline import SCHEMA_FILE_PATH
import pandas as pd
import os
from scipy.stats import ks_2samp
import sys
from mobile_price.utils.main_utils.utils import read_yaml_files,write_yaml_files



class DataValidation:
    def __init__(self,data_ingestiion_artifact: DataIngestionArtifact,
                 data_validation_config : DataValidationConfig):
        try:
            self.data_ingestiion_artifact = data_ingestiion_artifact
            self.data_validation_config = data_validation_config
            self.schema = read_yaml_files(SCHEMA_FILE_PATH)
        except Exception as e:
            raise PricingException(e,sys) from e
    def check_columns(self,df:pd.DataFrame) ->bool:
        try:
            no_of_columns = len(self.schema['columns'])
            logging.info(f"Number of columns in the schema: {no_of_columns}")
            logging.info(f"Number of columns in the dataframe: {len(df.columns)}")
            if no_of_columns == len(df.columns):
                return True
            else:
                return False
        except Exception as e:
            raise PricingException(e,sys) from e
    def check_numerical_columns(self,df:pd.DataFrame) ->bool:
        try:
            num_columns = len(self.schema['numerical_columns'])
            logging.info(f"Number of columns in the schema: {num_columns}")
            logging.info(f"Number of numerical columns in the dataframe: {len(df.select_dtypes(include=['number']).columns)}")
            if num_columns == len(df.select_dtypes(include=["number"]).columns):
                return True
            else:
                return False
        except Exception as e:
            raise PricingException(e,sys) from e
    @staticmethod
    def read_data(file_path)-> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise PricingException(e, sys) from e
    
    def check_dataset_drift(self,base_df,current_df,threshold = 0.05) -> bool:
        try:
            status = True
            report = {}

            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_same_dist = ks_2samp(d1,d2)
                if  threshold <= is_same_dist.pvalue:
                    is_found = False
                else:
                    is_found = True
                    status = False
                report.update({column:{
                        "p_value": is_same_dist.pvalue,
                        "is_found": is_found
                    }})
            drift_report_file_path  = self.data_validation_config.drift_report_file_path
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path, exist_ok=True)


            write_yaml_files(file_path=drift_report_file_path,content=report)
            return status
        except Exception as e:
            raise PricingException(e,sys) from e
    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            train_file_path = self.data_ingestiion_artifact.train_file_path
            test_file_path = self.data_ingestiion_artifact.test_file_path

            train_df = DataValidation.read_data(train_file_path)
            test_df = DataValidation.read_data(test_file_path)
            train_col_stat = self.check_columns(train_df)
            if not train_col_stat:
                logging.info("no of columns in train does not match with schema")
                print("no of columns in train does not match with schema")
            test_col_stat = self.check_columns(test_df)
            if not test_col_stat:
                logging.info("no of columns in test does not match with schema")
                print("no of columns in test does not match with schema")
            
            num_train_col_stat = self.check_numerical_columns(train_df)
            if not num_train_col_stat:
                logging.info("numerical columns in train does not match with schema")
                print("numerical columns in train does not match with schema")

            num_test_col_stat = self.check_numerical_columns(test_df)
            if not num_test_col_stat:
                logging.info("numerical columns in tesxt does not match with schema")
                print("numerical columns in test does not match with schema")
            
            status = self.check_dataset_drift(base_df=train_df,current_df=test_df)

            
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path, exist_ok=True)

            train_df.to_csv(self.data_validation_config.valid_train_file_path,index=False)
            test_df.to_csv(self.data_validation_config.valid_test_file_path,index=False)

            data_validation_artifact = DataValidationArtifact(
                    validation_status=status,
                    valid_train_file_path=  self.data_ingestiion_artifact.train_file_path,
                    valid_test_file_path= self.data_ingestiion_artifact.test_file_path,
                    invalid_train_file_path= None,
                    invalid_test_file_path= None,
                    drift_report_file_path=  self.data_validation_config.drift_report_file_path
                    
                )
            return data_validation_artifact
        except Exception as e:
            raise PricingException(e,sys) from e


