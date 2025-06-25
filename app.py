from flask import Flask, request, render_template
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from mobile_price.utils.ml_utils.model.estimator import NetworkModel
from mobile_price.pipeline.predict_pipeline import CustomData
from mobile_price.utils.main_utils.utils import load_object
from mobile_price.exception.exception import PricingException
import sys


application = Flask(__name__)
app = application

@app.route('/')
def Index():
    return render_template('index.html')

@app.route('/predictdata', methods=['GET','POST'])
def predict_datapoint():
    if request.method  == 'GET':
        return render_template('home.html')
    else:
        try:
            data = CustomData(
                battery_power=float(request.form.get('battery_power')),
                blue=float(request.form.get('blue')),
                clock_speed=float(request.form.get('clock_speed')),
                dual_sim=float(request.form.get('dual_sim')),
                fc=float(request.form.get('fc')),
                four_g=float(request.form.get('four_g')),
                int_memory=float(request.form.get('int_memory')),
                m_dep=float(request.form.get('m_dep')),
                mobile_wt=float(request.form.get('mobile_wt')),
                n_cores=float(request.form.get('n_cores')),
                pc=float(request.form.get('pc')),
                px_height=float(request.form.get('px_height')),
                px_width=float(request.form.get('px_width')),
                ram=float(request.form.get('ram')),
                sc_h=float(request.form.get('sc_h')),
                sc_w=float(request.form.get('sc_w')),
                talk_time=float(request.form.get('talk_time')),
                three_g=float(request.form.get('three_g')),
                touch_screen=float(request.form.get('touch_screen')),
                wifi=float(request.form.get('wifi'))
            )
            df = data.get_data_as_dataframe()
            print(df)
            preprocessor = load_object('final_model/preprocessing.pkl')
            model = load_object('final_model/model.pkl')
            ml_model = NetworkModel(preprocessor=preprocessor,model=model)

            results = ml_model.predict(df)
            print(results)

            prediction_value = results[0] if len(results) > 0 else None
            
            # Format the result to two decimal places if it's a float
            formatted_result = round(prediction_value, 2) if isinstance(prediction_value, float) else prediction_value
            print("Formatted Prediction result:", formatted_result)  # Debugging output
            return render_template('home.html', results=formatted_result)
        except Exception as e:
            raise PricingException(e, sys) from e

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
