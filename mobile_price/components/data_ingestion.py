import os
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import pymongo.mongo_client
load_dotenv()
from mobile_price.exception.exception import PricingException
from mobile_price.logging.logger import logging
from mobile_price.constants import training_pipeline
from mobile_price.entity.config_entity import DataIngestionConfig
from sklearn.model_selection import train_test_split
import pymongo
import sys
from mobile_price.entity.artifact_entity import DataIngestionArtifact

MONGO_DB_URL = os.getenv("MONGO_DB_URL")


class DataIngestion:
    def __init__(self,data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise PricingException(e,sys) from e
    def get_data_as_dataframe(self) ->pd.DataFrame:
        try:
            database_name = self.data_ingestion_config.database
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            collection = self.mongo_client[database_name][collection_name]
            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"],axis=1)
            df.replace({"na":np.nan},inplace=True)
            return df
        except Exception as e:
            raise PricingException(e,sys) from e
    def exprot_data_to_feature_store(self,df : pd.DataFrame):
        try:
            logging.info("exporting data to feature folder has satrted")
            feature_store_file_path = self.data_ingestion_config.feature_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            df.to_csv(feature_store_file_path,index=False,header=True)
            logging.info(f"Data exported to feature store at {feature_store_file_path}")
            return df
        except Exception as e:
            raise PricingException(e,sys) from e
    def split_data_as_train_test_split(self,df:pd.DataFrame):
        try:
            train_df,test_df = train_test_split(df,test_size=self.data_ingestion_config.train_test_split_ratio,random_state=42)
            logging.info("Performed tarin test split on the dataframe")

            train_file_path = self.data_ingestion_config.train_file_path
            test_file_path = self.data_ingestion_config.test_file_path
            dir_path = os.path.dirname(train_file_path)
            os.makedirs(dir_path,exist_ok=True)
            logging.info("File has been created sucessfully")

            train_df.to_csv(train_file_path,index = False,header=True)
            test_df.to_csv(test_file_path,index= False,header=True)
            logging.info("File has been saved sucessfully")

            return train_df,test_df
        except Exception as e:
            raise PricingException(e,sys) from e
        
    def initiate_data_ingestion(self)->DataIngestionArtifact:
        try:
            logging.info("Initialisation of data ingesgtiom has started")
            df = self.get_data_as_dataframe()
            df = self.exprot_data_to_feature_store(df)
            self.split_data_as_train_test_split(df=df)
            logging.info("Data ingestion completed successfully")
            data_ingestion_artifact = DataIngestionArtifact(
                train_file_path=self.data_ingestion_config.train_file_path,
                test_file_path= self.data_ingestion_config.test_file_path
            )
            return data_ingestion_artifact
        except Exception as e:
            raise PricingException(e,sys) from e


