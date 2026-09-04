 Python import network
import time
import ujson
from machine import Pin
import dht
from umqtt.simple import MQTTClient

# Wi-Fi & Broker Configuration
WIFI_SSID = "YOUR_WIFI_SSID"
WIFI_PASS = "YOUR_WIFI_PASSWORD"
MQTT_BROKER = "broker.hivemq.com" # or local IP
MQTT_PORT = 1883
MQTT_TOPIC = "iot/lab/sensor"
CLIENT_ID = "ESP32_DHT22_Node"

# Initialize Sensor
sensor = dht.DHT22(Pin(4))

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        wlan.connect(WIFI_SSID, WIFI_PASS)
        while not wlan.isconnected():
            time.sleep(0.5)
    print("Wi-Fi Connected:", wlan.ifconfig())

def connect_mqtt():
    client = MQTTClient(CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
    client.connect()
    print(f"Connected to MQTT Broker: {MQTT_BROKER}")
    return client

# Program Execution
connect_wifi()
mqtt_client = connect_mqtt()

while True:
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        
        payload = ujson.dumps({
            "temperature": round(temp, 2),
            "humidity": round(hum, 2)
        })mqtt_client.publish(MQTT_TOPIC, payload)
        print(f"Published to {MQTT_TOPIC}: {payload}")
    except Exception as e:
        print("Error reading sensor or publishing:", e)
        
    time.sleep(2)
