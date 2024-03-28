# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

ENV TZ=Asia/Singapore

# Copy the Python script and pickle file into the container
COPY final_sensor.csv quality_prediction.py PDF.py arima_co2.pickle arima_scaler_co2.pickle arima_scaler_humidity.pickle arima_scaler_temperature.pickle  arima_humidity.pickle arima_temperature.pickle /app/

# Install any needed dependencies specified in requirements.txt
# For example, if you use scikit-learn for your model, include it here
COPY requirements.txt /app/
COPY .env /app/.env
COPY resources /app/resources

RUN pip install --no-cache-dir -r requirements.txt

# Run the Python script when the container launches
CMD ["python", "quality_prediction.py"]