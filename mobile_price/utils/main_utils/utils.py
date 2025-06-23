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