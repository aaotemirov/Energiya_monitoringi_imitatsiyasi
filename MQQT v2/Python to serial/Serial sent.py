import serial
import json
import time
import paho.mqtt.client as mqtt

SERIAL_PORT = 'COM1'
BAUD = 9600

# Arduino Cloud Device API credentials (o'zingiznikiga almashtiring)
MQTT_BROKER = 'https://create.arduino.cc'   # to'g'ri broker host
MQTT_PORT = 8883
MQTT_USER = 'dac6eaa6-bf99-4c1a-a1ae-788c8e849b17'
MQTT_PASS = 'SBn22LGL8XdBo2eJoHHMA@6H6'
MQTT_TOPIC = 'v1/devices/me/telemetry'

ser = serial.Serial(SERIAL_PORT, BAUD, timeout=1)
time.sleep(2)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
client.username_pw_set(MQTT_USER, MQTT_PASS)
client.tls_set()   # TLS kerak bo'lsa
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

try:
    while True:
        line = ser.readline().decode('utf-8').strip()
        if ':' in line:
            k, v = line.split(':', 1)
            payload = {k: float(v)}
            client.publish(MQTT_TOPIC, json.dumps(payload))
            print('Sent', payload)
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    client.loop_stop()
    client.disconnect()
    ser.close()
