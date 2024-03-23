# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the Python script and pickle file into the container
COPY quality_prediction.py arima_co2.pickle arima_humidity.pickle arima_temperature.pickle /app/

# Install any needed dependencies specified in requirements.txt
# For example, if you use scikit-learn for your model, include it here
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

# Run the Python script when the container launches
CMD ["python", "quality_prediction.py"]