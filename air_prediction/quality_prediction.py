import pickle
from flask import Flask, request

app = Flask(__name__)

# Open the pickle file and load the model
with open('arima_co2.pickle', 'rb') as file:
    model = pickle.load(file)

@app.route('/predict', methods=['POST'])
def predict():
    # Receive the data from Node-RED
    data = request.get_data()

    if data:
        # Process the received data using the model
        result = model.predict(data)  # Assuming 'model' has a predict method
        print('Received data:', data)
        print('Prediction result:', result)
        return str(result)  # Return the prediction result as a response
    else:
        return 'No data received'

if __name__ == '__main__':
    app.run(debug=True,port = 5000,host='0.0.0.0')
