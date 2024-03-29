import pickle
import numpy as np

from datetime import datetime, timedelta
from flask import Flask, request,send_file
from PDF import PDF
import os
import time

import paho.mqtt.client as mqtt






app = Flask(__name__)

count = 1
next_timestamp = (datetime.now() + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0).strftime('%Y-%m-%d %H:%M:%S')

co2_threshold = 800
temperture_threshold = 27
humidity_threshold = 65

# Open the pickle file and load the model
with open('arima_co2.pickle', 'rb') as file:
    co2_model = pickle.load(file)

with open('arima_scaler_co2.pickle', 'rb') as file:
    co2_scaler = pickle.load(file)

with open('arima_scaler_humidity.pickle', 'rb') as file:
    humidity_scaler = pickle.load(file)

with open('arima_scaler_temperature.pickle','rb') as file:
    temperature_scaler = pickle.load(file)

with open('arima_humidity.pickle','rb') as file:
    humidity_model = pickle.load(file)
with open('arima_temperature.pickle','rb') as file:
    temperature_model = pickle.load(file)

mqttc = None
broker_address = "test.mosquitto.org"
port = 1883
topic_on = "iot/sensor1/on"
topic_off = "iot/sensor1/off"

def turnOn() -> None:
    global mqttc

    mqttc = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION1)
    mqttc.connect(broker_address, port)
    mqttc.loop_start()
    payload="on"
    print(f"Publish | topic: {topic_on} | payload: {payload}")
    mqttc.publish(topic=topic_on, payload=payload, qos=2)
    time.sleep(5)
    mqttc.loop_stop()
    print("turn on")
def turnOff() -> None:
    global mqttc
    print("hello")

    mqttc = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION1)
    mqttc.connect(broker_address, port)
    mqttc.loop_start()
    payload="off"
    print(f"Publish | topic: {topic_off} | payload: {payload}")
    mqttc.publish(topic=topic_off, payload=payload, qos=2)
    time.sleep(5)
    mqttc.loop_stop()

@app.route('/predict', methods=['GET'])
def predict():
    metircs = 0
    status = ''
    global count, next_timestamp
    
    # Update count and next_timestamp if an hour has passed
    current_time = datetime.now()
    if current_time >= datetime.strptime(next_timestamp, '%Y-%m-%d %H:%M:%S'):
        count += 1
        next_timestamp = (current_time + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0).strftime('%Y-%m-%d %H:%M:%S')

    pred_co2 = co2_model.forecast(steps=count)[0]

    co2_result = round(co2_scaler.inverse_transform(np.array(pred_co2).reshape(-1, 1))[0][0], 1)
    
    if co2_result >co2_threshold:
        metircs +=1
    
    pred_humidity = humidity_model.forecast(steps=count)[0]
    
    humidity_result  = round(humidity_scaler.inverse_transform(np.array(pred_humidity).reshape(-1, 1))[0][0], 1)
    if humidity_result > humidity_threshold:
        metircs +=1
    
    pred_temperature = temperature_model.forecast(steps=count)[0]
    temperature_result = round(temperature_scaler.inverse_transform(np.array(pred_temperature).reshape(-1, 1))[0][0], 1)
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
    # Next Predicted hour will be bad
    if metircs <2:
        turnOff()
    # Next predicted hour will be good
    else:

        turnOn()

    # print('Prediction result:', co2_result)
    
    # print(temperature_result)
    return {
        'Next Predicted Time': next_timestamp,
        'CO2 ' : co2_result,
        'Humidity' : humidity_result,
        'Temperature' :  temperature_result,
        'Status' : status
    }  # Return the prediction result as a response
        
    
@app.route('/report',methods  =['POST'])
def generate_report():
    type_of_report = request.args.get('type')
    data = request.json



    
    
    pdf = PDF() # A4 (210 by 297 mm)
    pdf.setup(data)
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
    pdf.ln(130)
    # Replace this with chatgpt input for the analysis
    pdf.write_to_pdf(pdf.analysis('./resources/temperature.png','Can you give me an insight into the trends of these plots?'))



    # Add another Page
    pdf.add_page()
    pdf.ln(10)
    pdf.write_heading_pdf(f"Graph Of Carbon Dioxide vs Time For the Past {type_of_report.capitalize()} Days ")
    pdf.ln(5)
    pdf.write_to_pdf("Through this graph, we can see if there are timings that are above the red threshold of 800ppm for CO2 readings ")
    
    pdf.co2_trend_analysis()
    pdf.image("./resources/CO2.png",0,30,210)
    pdf.ln(130)
    pdf.write_to_pdf(pdf.analysis('./resources/CO2.png','Can you give me an insight into the trends of these plots?'))

    pdf.add_page()
    
    pdf.ln(10)
    pdf.write_heading_pdf(f"Graph Of Humidity vs Time For the Past {type_of_report.capitalize()} Days ")
    pdf.ln(5)
    pdf.write_to_pdf("Through this graph, we can see if there are timings that are above the red threshold of 65(%) for Humidity readings ")
    pdf.humidity_trend_analysis()
    pdf.image('./resources/Humidity.png',0,30,210)
    pdf.ln(130)
    pdf.write_to_pdf(pdf.analysis('./resources/Humidity.png','Can you give me an insight into the trends of these plots?'))
    pdf.ln(10)
   
    # Set up for Ambient Air Composition Analysis
    pdf.ambient_air_setup()
    # save all the images in a folder for ambient air analysis
    pdf.plot_pie_chart()
    folder_path = "./resources/piecharts"
    pdf.add_page()
    pdf.write_heading_pdf(f"Ambient Air Composition Analysis ")
    pdf.ln(10)


    pdf.image('./resources/air_composition.png',5,15,210)
    index = 0
    pdf.ln(45)
    pdf.write_heading_pdf(f"Distribution of Air Quality for all Sensors")
    for  file in ( os.listdir(folder_path)):

       
        pdf.image(os.path.join(folder_path,file),70,90+index*75,70,70)
        

        index +=1
        if index %2 ==0 and index!=0:
            # Add a page and then reset the index to 1

            pdf.add_page() 
            index =-1
  
    pdf.plot_time_chart()
    folder_path = folder_path = "./resources/air_quality_plots"
    index =0
    
    pdf.write_heading_pdf(f"Distribution of Air Quality in Hours for All Sensors")
    for  file in ( os.listdir(folder_path)):

       
        pdf.image(os.path.join(folder_path,file),40,20+index*135,130,130)
        
        index +=1
        if index %2 ==0 and index!=0:
            # Add a page and then reset the index to 1

            pdf.add_page() 
            index =0
    pdf.ln(180)
    pdf.write_to_pdf(pdf.analyse_list_images())
    


    
    
    
        

    



    
    pdf.output("resources/Trend_Problem_Analysis_report.pdf", 'F')
    
    return send_file('resources/Trend_Problem_Analysis_report.pdf')

    

 


    
  







if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')
