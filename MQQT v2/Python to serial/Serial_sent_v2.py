import serial
import json
import time
import paho.mqtt.client as mqtt
import certifi
import logging
import socket
import sys
from arduino_iot_cloud import ArduinoCloudClient

# ---------- Sozlamalar (o'zingizga moslang) ----------
SERIAL_PORT = 'COM3'        # Proteus virtual COM portni kiriting
BAUD = 9600

MQTT_BROKER = 'mqtts.iot.arduino.cc'
MQTT_PORT = 8883
MQTT_USER = '834c57a9-28e6-4f9b-9be3-1f5b09c0af7c'        # Manual Device ID
MQTT_PASS = '6s7n3WCNNG9FRELlKIh?LzNQ3'    # Manual Device Secret
# ----------------------------------------------------

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("bridge")

# DNS tekshiruvi (tez diagnostika)
try:
    logger.info(f"Resolving {MQTT_BROKER} ...")
    socket.getaddrinfo(MQTT_BROKER, MQTT_PORT)
except socket.gaierror as e:
    logger.error(f"DNS resolution failed for {MQTT_BROKER}: {e}")
    sys.exit(1)

# Serialga ulanish
try:
    ser = serial.Serial(SERIAL_PORT, BAUD, timeout=1)
    time.sleep(2)
except Exception as e:
    logger.error(f"Serial portga ulanishda xato: {e}")
    sys.exit(1)

# MQTT client (callback API ogohlantirishini bartaraf etish uchun)
client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION1)
client.enable_logger()
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("MQTT connected successfully")
    else:
        logger.error(f"MQTT connect failed with rc={rc}")
def on_disconnect(client, userdata, rc):
    logger.info(f"MQTT disconnected rc={rc}")

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.username_pw_set(MQTT_USER, MQTT_PASS)

# TLS: tizim CA sertifikatlari orqali
try:
    client.tls_set(ca_certs=certifi.where())
except Exception as e:
    logger.warning(f"TLS sozlashda ogohlantirish: {e}")

# Ulanish
try:
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
except Exception as e:
    logger.error(f"MQTT ga ulanishda xato: {e}")
    ser.close()
    sys.exit(1)

client.loop_start()

try:
    while True:
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        if not line:
            time.sleep(0.1)
            continue
        logger.info(f"Serial: {line}")
        if ':' in line:
            k, v = line.split(':', 1)
            try:
                payload = {k: float(v)}
            except ValueError:
                logger.warning(f"Qiymatni float ga aylantirishda xato: {v}")
                continue
            client.publish(MQTT_TOPIC, json.dumps(payload))
            logger.info(f"Published {payload} to {MQTT_TOPIC}")
        time.sleep(0.5)
except KeyboardInterrupt:
    logger.info("To'xtatildi (Ctrl+C)")
finally:
    client.loop_stop()
    client.disconnect()
    ser.close()
    logger.info("Tugatildi")
