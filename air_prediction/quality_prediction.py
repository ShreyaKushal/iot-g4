import pickle
import numpy as np

from datetime import datetime, timedelta
from flask import Flask, request,send_file
from PDF import PDF





app = Flask(__name__)

count = 1
next_timestamp = (datetime.now() + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0).strftime('%Y-%m-%d %H:%M:%S')

co2_threshold = 800
temperture_threshold = 27
humidity_threshold = 65

# Open the pickle file and load the model
with open('arima_co2.pickle', 'rb') as file:
    co2_model = pickle.load(file)

with open('arima_scaler.pickle', 'rb') as file:
    scaler = pickle.load(file)
with open('arima_humidity.pickle','rb') as file:
    humidity_model = pickle.load(file)
with open('arima_temperature.pickle','rb') as file:
    temperature_model = pickle.load(file)

@app.route('/predict', methods=['POST'])
def predict():
    metircs = 0
    status = ''
    global count, next_timestamp
    
    # Update count and next_timestamp if an hour has passed
    current_time = datetime.now()
    if current_time >= datetime.strptime(next_timestamp, '%Y-%m-%d %H:%M:%S'):
        count += 1
        next_timestamp = (current_time + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0).strftime('%Y-%m-%d %H:%M:%S')

    # Receive the data from Node-RED
    data = request.get_data()

    if data:
        # Process the received data using the model
        pred_co2 = co2_model.forecast(steps=count)[0]
        co2_result = round(scaler.inverse_transform(np.array(pred_co2).reshape(-1, 1))[0][0], 1)
        if co2_result >co2_threshold:
            metircs +=1
        
        pred_humidity = humidity_model.forecast(steps=count)[0]
        humidity_result  = round(scaler.inverse_transform(np.array(pred_humidity).reshape(-1, 1))[0][0], 1)
        if humidity_result > humidity_threshold:
            metircs +=1
        
        pred_temperature = temperature_model.forecast(steps=count)[0]
        temperature_result = round(scaler.inverse_transform(np.array(pred_temperature).reshape(-1, 1))[0][0], 1)
        if temperature_result > temperture_threshold:
            metircs +=1
        if metircs == 0:
            status = "Good"
        elif metircs == 1:
            status = "Moderate High"
        elif metircs == 2:
            status ="Moderate Low"
        else:
            status = "Bad"



        print('Received data:', data)
        print('Prediction result:', co2_result)
        return {
            'Next Predicted Time': next_timestamp,
            'CO2 ' : co2_result,
            'Humidity' : humidity_result,
            'Temperature' :  temperature_result,
            'Status' : status
        }  # Return the prediction result as a response
    else:
        return 'No data received'
@app.route('/report',methods  =['GET'])
def generate_report():
    type_of_report = request.args.get('type')

    # Have to generate the title better 

# Open the data
    
    
    
  

# Set the style of seaborn for better visualization
    

# Plotting
    

    
    pdf = PDF() # A4 (210 by 297 mm)
    pdf.setup()
    pdf.add_page()
    pdf.create_letterhead()
    pdf.create_title(type_of_report)
    pdf.temperature_trend_analysis()
    pdf.ln(10)
    pdf.write_heading_pdf(f"Graph Of Temperature vs Time For the Past {type_of_report.capitalize()} Days ")
    pdf.ln(5)
    pdf.write_to_pdf("Through this graph, we can see if there are timings that are above the red threshold of (27.C) for temperature readings ")
    # Temperature Graph
    pdf.image("./resources/temperature.png",0,100,210)
    # Add another Page
    pdf.add_page()
    pdf.ln(10)
    pdf.write_heading_pdf(f"Graph Of Carbon Dioxide vs Time For the Past {type_of_report.capitalize()} Days ")
    pdf.ln(5)
    pdf.write_to_pdf("Through this graph, we can see if there are timings that are above the red threshold of 800ppm for CO2 readings ")

    pdf.co2_trend_analysis()
    pdf.image("./resources/CO2.png",0,30,210)
    pdf.humidity_trend_analysis()
    pdf.ln(120)
    pdf.write_heading_pdf(f"Graph Of Humidity vs Time For the Past {type_of_report.capitalize()} Days ")
    pdf.ln(5)
    pdf.write_to_pdf("Through this graph, we can see if there are timings that are above the red threshold of 65(%) for Humidity readings ")

    pdf.image('./resources/Humidity.png',0,158,210)
    pdf.output("resources/Trend_Problem_Analysis_report.pdf", 'F')
    return send_file('resources/Trend_Problem_Analysis_report.pdf')
    

 


    
  







if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
