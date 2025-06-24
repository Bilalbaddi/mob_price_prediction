import os
from mobile_price.exception.exception import PricingException
from mobile_price.logging.logger import logging
import pandas as pd
import numpy as np
import yaml
import sys
import pickle
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import r2_score
from sklearn.metrics import accuracy_score




def read_yaml_files(file_path:str) ->dict:
    try:
        with open(file_path,'rb') as file:
            return yaml.safe_load(file)
    except Exception as e:
        raise PricingException(e,sys) from e
    
def write_yaml_files(file_path:str,content:object,replace : bool = False)-> None:
    try:
           if replace :
            if os.path.exists(file_path):
                os.remove(file_path)
            os.makedirs(os.path.dirname(file_path),exist_ok=True)
            with open(file_path,"wb") as file:
                yaml.dump(file)
    except Exception as e:
        raise PricingException(e,sys) from e
    
def save_object(file_path:str,obj:object)->None:
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,'wb') as file:
            pickle.dump(obj,file)
    except Exception as e:
        raise PricingException(e,sys) from e
    
def save_numpy_array(file_path:str,array:np.ndarray) -> None:
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,'wb') as file:
            np.save(file,array)
    except Exception as e:
        raise PricingException(e,sys) from e
    
def load_object(file_path:str):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        with open(file_path,"rb") as file:
            return pickle.load(file)
    except Exception as e:
        raise PricingException(e,sys) from e

def load_numpy_array(file_path:str) -> np.array:
    try:
        with open(file_path,"rb") as file:
            return  np.load(file)
        logging.info("File loadede sucessfully")
    except Exception as e:
        raise PricingException(e,sys) from e
    
def evaluate_model(x_train,y_train,x_test,y_test,models):
    try:
        reports = {}
        for i in range(len(list(models))):
            model = list(models.values())[i]
            # para = params[list(models.keys())[i]]

            # rs = RandomizedSearchCV(model,para,cv=4)
            # rs.fit(x_train,y_train)

            # model.set_params(**rs.best_params_)
            model.fit(x_train,y_train)

            y_train_pred = model.predict(x_train)
            y_test_pred = model.predict(x_test)

            train_model_score = r2_score(y_train,y_train_pred)
            test_model_score = r2_score(y_test,y_test_pred)


            reports[list(models.keys())[i]] = test_model_score
        

        return reports
    except Exception as e:
        raise PricingException(e,sys) from e 
    