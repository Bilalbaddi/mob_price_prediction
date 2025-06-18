import os
import pymongo
import pandas as pd
import numpy as np
import pymongo.max_staleness_selectors

from mobile_price.exception.exception import PricingException
from mobile_price.logging.logger import logging

import json
import sys
from dotenv import load_dotenv
load_dotenv()

import certifi
ca = certifi.where()

MONGO_DB_URL = os.getenv('MONGO_DB_URL')
print(MONGO_DB_URL)
class DataExtract:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise PricingException(e,sys) from e
        
    def csv_to_json(self,file_path):
        try:
            df = pd.read_csv(file_path)
            df.reset_index(drop=True,inplace=True)
            records = list(json.loads(df.T.to_json()).values())
            return records
        except Exception as e:
            raise PricingException(e,sys) from e
    def insert_data_to_mongo_db(self,records,collection,database):
        try:
            self.records = records
            self.database = database
            self.collection = collection
            self.client = pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.client[self.database]
            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)
            return(len(self.records))
        except Exception as e:
            raise PricingException(e,sys) from e

if __name__ == "__main__":
    FILE_PATH = "data\dataset.csv"
    DATABASE = "pricingdb"
    collection = "mobile_pricing_data"
    networkobj = DataExtract()
    records = networkobj.csv_to_json(file_path=FILE_PATH)
    print(records)
    no_of_records = networkobj.insert_data_to_mongo_db(records, DATABASE, collection)
    print(no_of_records)
    