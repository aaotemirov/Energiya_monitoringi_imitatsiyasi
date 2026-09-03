import serial
import time
import logging
import sys
from arduino_iot_cloud import ArduinoCloudClient

# ---------- Sozlamalar ----------
SERIAL_PORT = 'COM3'        # Proteus virtual COM porti
BAUD = 9600

DEVICE_ID = "834c57a9-28e6-4f9b-9be3-1f5b09c0af7c"
SECRET_KEY = "6s7n3WCNNG9FRELlKIh?LzNQ3"
# --------------------------------

# Loglarni chiroyli ko'rsatish uchun sozlama
logging.basicConfig(datefmt="%H:%M:%S", format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger("ArduinoCloud")

# Serial portga ulanish
try:
    ser = serial.Serial(SERIAL_PORT, BAUD, timeout=1)
    time.sleep(2)
    logger.info(f"Serial port {SERIAL_PORT} muvaffaqiyatli ochildi.")
except Exception as e:
    logger.error(f"Serial portga ulanishda xato: {e}")
    sys.exit(1)

# Arduino Cloud mijozini yaratish (Ulanish va sertifikatlar avtomatik bajariladi)
client = ArduinoCloudClient(device_id=DEVICE_ID, username=DEVICE_ID, password=SECRET_KEY)

# Platformadagi 'Temperature' o'zgaruvchisini Python kodiga ro'yxatdan o'tkazamiz
# Diqqat: Arduino qoidasiga ko'ra o'zgaruvchi nomi kichik harflarda 'temperature' deb yoziladi
client.register("temperature", value=0.0)

# Bulutga muvaffaqiyatli ulanganda ishlovchi funksiya
def on_connect(client):
    logger.info("Arduino IoT Cloud platformasiga muvaffaqiyatli ulandi!")

client.on_connect = on_connect

# Fon rejimida ulanishni boshlash
logger.info("Bulutga ulanish jarayoni boshlandi...")
client.start()

try:
    while True:
        # Serialdan ma'lumotni o'qish
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        if not line:
            time.sleep(0.1)
            continue
        
        logger.info(f"Proteus'dan kelgan xabar: {line}")
        
        # Proteus'dan "harorat:25.4" yoki "Temperature:30" formatida kelishi kerak
        if ':' in line:
            k, v = line.split(':', 1)
            try:
                harorat_qiymati = float(v)
                
                # ENG OSON QISM: Shunchaki qiymatni o'zgaruvchiga yuklaymiz.
                # Kutubxona buni o'zi avtomatik ravishda Arduino Cloud'ga jo'natadi!
                client["temperature"] = harorat_qiymati
                logger.info(f"Bulutga yuborildi: {harorat_qiymati}°C")
                
            except ValueError:
                logger.warning(f"Kelgan qiymatni songa (float) o'girib bo'lmadi: {v}")
        
        time.sleep(0.5)

except KeyboardInterrupt:
    logger.info("Dastur foydalanuvchi tomonidan to'xtatildi.")
finally:
    client.stop()
    ser.close()
    logger.info("Aloqa uzildi va dastur yakunlandi.")
