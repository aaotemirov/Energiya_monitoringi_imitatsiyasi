import socket
import logging
import time
import json
import serial
import paho.mqtt.client as mqtt
import certifi
import sys

# Sozlamalar
SERIAL_PORT = 'COM3'
BAUD = 9600

MQTT_BROKER = 'mqtts.iot.arduino.cc'
MQTT_PORT = 8883
MQTT_USER = 'ef6e9244-3b98-4270-8de2-827b3a6821df'
MQTT_PASS = 'O#qd#0yyyiyWlDtaHPb5sL!Rq'
MQTT_TOPIC = 'v1/devices/me/telemetry'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("bridge")

# Global socket timeout (sekundlarda) — connect vaqtini oshirish uchun
socket.setdefaulttimeout(15)

def on_connect(client, userdata, flags, rc):
    logger.info(f"on_connect rc={rc}")

def on_disconnect(client, userdata, rc):
    logger.info(f"on_disconnect rc={rc}")

def on_log(client, userdata, level, buf):
    logger.debug(f"MQTT log: {buf}")

client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION1)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_log = on_log
client.username_pw_set(MQTT_USER, MQTT_PASS)

# TLS
try:
    client.tls_set(ca_certs=certifi.where())
except Exception as e:
    logger.warning(f"TLS sozlashda ogohlantirish: {e}")

# Qayta ulanish sozlamalari
client.reconnect_delay_set(min_delay=1, max_delay=120)

# Avval DNS va portni tekshirish (tez diagnostika)
try:
    logger.info(f"Resolving {MQTT_BROKER} ...")
    addrs = socket.getaddrinfo(MQTT_BROKER, MQTT_PORT)
    logger.info(f"Address info: {addrs[0][4]}")
except Exception as e:
    logger.error(f"DNS/resolve error: {e}")
    # Vaqtinchalik test: umumiy brokerga ulanishni sinab ko'ramiz
    logger.info("Arduino brokeriga ulanishda muammo. Test brokerga ulanish sinovi boshlanadi.")
    try:
        client.connect('test.mosquitto.org', 1883, 60)
        client.loop_start()
        logger.info("Test brokerga ulanishga urinish yuborildi (test.mosquitto.org:1883).")
    except Exception as e2:
        logger.error(f"Test brokerga ham ulanishda xato: {e2}")
    sys.exit(1)

# Serialga ulanish
try:
    ser = serial.Serial(SERIAL_PORT, BAUD, timeout=1)
    time.sleep(2)
except Exception as e:
    logger.error(f"Serial portga ulanishda xato: {e}")
    sys.exit(1)

# Asl brokerga ulanish (agar DNS muvaffaqiyatli bo'lsa)
try:
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()
except Exception as e:
    logger.error(f"MQTT ga ulanishda xato: {e}")
    # Qo'shimcha: agar TLS bilan muammo bo'lsa, test brokerga qayta urin
    try:
        client.connect('test.mosquitto.org', 1883, 60)
        client.loop_start()
        logger.info("Test brokerga ulanishga urinish yuborildi (test.mosquitto.org:1883).")
    except Exception as e2:
        logger.error(f"Test brokerga ham ulanishda xato: {e2}")
    sys.exit(1)

# Keyingi qadam: serial o'qish va publish (sizning mavjud kodni shu yerga qo'ying)
