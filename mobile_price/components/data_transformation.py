import os
import sys
import pandas as pd
from mobile_price.exception.exception import PricingException
from mobile_price.logging.logger import logging
import numpy as np
from mobile_price.constants.training_pipeline import TARGET_COLUMN_NAME
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from mobile_price.entity.artifact_entity import(
    DataTransformationArtifact,
    DataIngestionArtifact,
    DataValidationArtifact
)
from mobile_price.entity.config_entity import DataTransformationConfig

from mobile_price.utils.main_utils.utils import save_numpy_array,save_object
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from  imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline



class DataTransformation:
    def __init__(self,data_validation_artifact : DataIngestionArtifact,
                 data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact : DataValidationArtifact = data_validation_artifact
            self.data_transformation_config : DataTransformationConfig = data_transformation_config
        except Exception as e:
            raise PricingException(e,sys) from e
    @staticmethod
    def read_data(file_path)-> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise PricingException(e, sys) from e
    def get_data_transformation(self):
        try:
            scaler : StandardScaler = StandardScaler()
            pca : PCA = PCA(n_components=4)

            pipeline : Pipeline= Pipeline(
                steps=[
                    ('scaler',scaler),
                    ('pca',pca)
                ]
            )
            return pipeline
        except Exception as e:
            raise PricingException(e,sys) from e
    def initiate_data_transformation(self):
        try:
            train_df_file_path = self.data_validation_artifact.valid_train_file_path
            test_df_file_path = self.data_validation_artifact.valid_test_file_path

            train_df = self.read_data(train_df_file_path)
            test_df = self.read_data(test_df_file_path)

            train_input_feature = train_df.drop(columns=TARGET_COLUMN_NAME,axis=1)
            target_train_feature = train_df[TARGET_COLUMN_NAME]

            input_test_feature_df = test_df.drop(columns=[TARGET_COLUMN_NAME],axis=1)
            target_test_feature_df = test_df[TARGET_COLUMN_NAME]


            preprocessor = self.get_data_transformation()
            pre_obj = preprocessor.fit(train_input_feature)

            transformed_input_train_feature = pre_obj.transform(train_input_feature)
            transformed_input_test_feature = pre_obj.transform(input_test_feature_df)

            train_arr = np.c_[transformed_input_train_feature, np.array(target_train_feature)]
            test_arr = np.c_[transformed_input_test_feature, np.array(target_test_feature_df)]

            save_numpy_array(file_path=self.data_transformation_config.train_transformed_file_path,array=train_arr)
            save_numpy_array(file_path = self.data_transformation_config.test_transformed_file_path,array=test_arr)
            save_object(file_path=self.data_transformation_config.transformed_object_file_path,obj=pre_obj)

            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                train_transformed_file_path= self.data_transformation_config.train_transformed_file_path,
                test_transformed_file_path = self.data_transformation_config.test_transformed_file_path
            )
            return data_transformation_artifact
        except Exception as e:
            raise PricingException(e,sys) from e

        


