import pandas as pd
from mobile_price.utils.main_utils.utils import load_object
from mobile_price.exception.exception import PricingException
import sys


import pandas as pd
import sys
from mobile_price.exception.exception import PricingException

class CustomData:
    def __init__(self,
                 battery_power: int,
                 blue: int,
                 clock_speed: float,
                 dual_sim: int,
                 fc: int,
                 four_g: int,
                 int_memory: int,
                 m_dep: float,
                 mobile_wt: int,
                 n_cores: int,
                 pc: int,
                 px_height: int,
                 px_width: int,
                 ram: int,
                 sc_h: int,
                 sc_w: int,
                 talk_time: int,
                 three_g: int,
                 touch_screen: int,
                 wifi: int):
        try:
            self.battery_power = battery_power
            self.blue = blue
            self.clock_speed = clock_speed
            self.dual_sim = dual_sim
            self.fc = fc
            self.four_g = four_g
            self.int_memory = int_memory
            self.m_dep = m_dep
            self.mobile_wt = mobile_wt
            self.n_cores = n_cores
            self.pc = pc
            self.px_height = px_height
            self.px_width = px_width
            self.ram = ram
            self.sc_h = sc_h
            self.sc_w = sc_w
            self.talk_time = talk_time
            self.three_g = three_g
            self.touch_screen = touch_screen
            self.wifi = wifi
        except Exception as e:
            raise PricingException(e, sys) from e

    def get_data_as_dataframe(self) -> pd.DataFrame:
        try:
            custom_data_input_dict = {
                "battery_power": [self.battery_power],
                "blue": [self.blue],
                "clock_speed": [self.clock_speed],
                "dual_sim": [self.dual_sim],
                "fc": [self.fc],
                "four_g": [self.four_g],
                "int_memory": [self.int_memory],
                "m_dep": [self.m_dep],
                "mobile_wt": [self.mobile_wt],
                "n_cores": [self.n_cores],
                "pc": [self.pc],
                "px_height": [self.px_height],
                "px_width": [self.px_width],
                "ram": [self.ram],
                "sc_h": [self.sc_h],
                "sc_w": [self.sc_w],
                "talk_time": [self.talk_time],
                "three_g": [self.three_g],
                "touch_screen": [self.touch_screen],
                "wifi": [self.wifi]
            }
            return pd.DataFrame(custom_data_input_dict)
        except Exception as e:
            raise PricingException(e, sys) from e
