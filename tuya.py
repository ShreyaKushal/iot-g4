# pip install paho-mqtt

import paho.mqtt.client as mqtt
import time

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

def turnOff() -> None:
    global mqttc

    mqttc = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION1)
    mqttc.connect(broker_address, port)
    mqttc.loop_start()
    payload="off"
    print(f"Publish | topic: {topic_off} | payload: {payload}")
    mqttc.publish(topic=topic_off, payload=payload, qos=2)
    time.sleep(5)
    mqttc.loop_stop()

if __name__ == "__main__":
    turnOn()
   #turnOff()