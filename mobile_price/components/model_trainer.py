import os
import sys
import pandas as pd
import numpy as np
from mobile_price.exception.exception import PricingException
from mobile_price.logging.logger import logging
from mobile_price.entity.config_entity import ModelTrainerConfig
from mobile_price.entity.artifact_entity import (
    DataTransformationArtifact,
    ModelTrainerArtifact
)
from mobile_price.utils.main_utils.utils import  save_object,load_object
from mobile_price.utils.main_utils.utils import  load_numpy_array,evaluate_model
from mobile_price.utils.ml_utils.metric.classification_metrics import get_classification_metrics
from mobile_price.utils.ml_utils.model.estimator import NetworkModel

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    RandomForestClassifier,
    GradientBoostingClassifier,
    AdaBoostClassifier
)
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

from sklearn.model_selection import RandomizedSearchCV
import mlflow
import dagshub



class ModelTrainer:
    def __init__(self,data_transformation_artifact : DataTransformationArtifact,
                 model_trainner_config: ModelTrainerConfig ):
        try:
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainner_config = model_trainner_config
        except Exception as e:
            raise PricingException(e,sys) from e
    def train_model(self,x_train,y_train,x_test,y_test):
       try:
            models = {
                    "RandomForestClassifier" : RandomForestClassifier(),
                    "GradientBoostingClassifier" : GradientBoostingClassifier(),
                    "AdaBoostClassifier": AdaBoostClassifier(),
                    "LogisticRegression" : LogisticRegression(solver='lbfgs', max_iter=1000),
                    "DecisionTreeClassifier" : DecisionTreeClassifier(),
                    "KNeighborsClassifier" : KNeighborsClassifier(),
                    "SVC" : SVC()
                }
            model_report :dict = evaluate_model(x_train=x_train,y_train=y_train,x_test=x_test,y_test=y_test,models=models)
            best_model_score = max(sorted(model_report.values()))

            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model = models[best_model_name]

            y_train_pred = best_model.predict(x_train)
            classification_train_matrix = get_classification_metrics(y_true=y_train,y_pred=y_train_pred)
            
            y_test_pred = best_model.predict(x_test)
            classification_test_matrix = get_classification_metrics(y_true=y_test,y_pred=y_test_pred)
            print(classification_test_matrix)

            preprocessor = load_object(self.data_transformation_artifact.transformed_object_file_path)
            model_dir_path = os.path.dirname(self.model_trainner_config.trained_model_file_path)
            os.makedirs(model_dir_path,exist_ok=True)

            model = NetworkModel(preprocessor=preprocessor,model=best_model)
            save_object(file_path=self.model_trainner_config.trained_model_file_path,obj=model)

            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=self.model_trainner_config.trained_model_file_path,
                train_metric_artifact=classification_train_matrix,
                test_metric_artifact= classification_test_matrix

            )
            return model_trainer_artifact
       except Exception as e:
           raise PricingException(e,sys) from e
    
    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            train_path = self.data_transformation_artifact.train_transformed_file_path
            test_path = self.data_transformation_artifact.test_transformed_file_path

            train_arr = load_numpy_array(file_path=train_path)
            test_arr = load_numpy_array(file_path=test_path)

            x_train,y_train,x_test,y_test = (
                train_arr[:,:-1],
                train_arr[:, -1],
                test_arr[:,:-1],
                test_arr[:, -1],
            )
            model_trainer_artifact = self.train_model(x_train=x_train,x_test=x_test,y_train=y_train,y_test=y_test)
            return model_trainer_artifact
        except Exception as e:
            raise PricingException(e,sys) from e