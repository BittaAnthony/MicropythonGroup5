Python import json
import sqlite3
import paho.mqtt.client as mqtt

DB_NAME = "sensor_data.db"
BROKER = "broker.hivemq.com"
TOPIC = "iot/lab/sensor"

# Database Initialization
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            temperature REAL,
            humidity REAL
        )
    ''')
    conn.commit()
    conn.close()

def save_to_db(temp, hum):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO readings (temperature, humidity)
        VALUES (?, ?)
    ''', (temp, hum))
    conn.commit()
    conn.close()
    print(f"[DB] Persisted -> Temp: {temp}°C | Humidity: {hum}%")

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    print(f"Connected to Broker with result code: {rc}")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode('utf-8'))
        temp = data.get("temperature")
        hum = data.get("humidity")
        print(f"[MQTT Recv] {msg.topic}: {data}")
        save_to_db(temp, hum)
    except Exception as e:
        print("Failed to process message:", e)

init_db()
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, 1883, 60)
client.loop_forever()
