from mobile_price.constants.training_pipeline import SAVED_MODEL_DIR, SAVED_MODEL_NAME

from mobile_price.exception.exception import PricingException
from mobile_price.utils.main_utils.utils import load_object, save_object
import sys
import os


class NetworkModel:
    
    def __init__(self,preprocessor,model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            raise PricingException(e, sys) from e
    def predict(self,x):
        try:
            x_transform = self.preprocessor.transform(x)
            y_hat = self.model.predict(x_transform)
        except Exception as e:
            raise PricingException(e, sys) from e
        return y_hat