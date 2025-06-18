from mobile_price.logging.logger import logging
import os
import sys


def get_error_message(error,error_detail:sys):
    _,_,exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_meesage = "Error occured in python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name,exc_tb.tb_lineno,str(error))
    return error_meesage

class PricingException(Exception):
    def __init__(self,error_message,error_detail:sys):
        super().__init__(error_message)
        self.error_message = get_error_message(error=error_message,error_detail=error_detail)

    def __str__(self):
        return self.error_message
    
if __name__ == "__main__":
    try:
        logging.info("Enter try block")
        a = 1/0
        print("item will nt be printed",a)
    except Exception as e:
        raise PricingException(e,sys) from e
    