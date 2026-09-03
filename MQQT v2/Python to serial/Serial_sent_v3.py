import time
import logging
from datetime import datetime
import sys
import json

# agar arduino_iot_cloud modulini 'lib' papkadan yuklayotgan bo'lsangiz
sys.path.append("lib")
from arduino_iot_cloud import ArduinoCloudClient

# Serial kutubxonasi
import serial

# ---------- Sozlamalarni o'zgartiring ----------
SERIAL_PORT = 'COM3'         # Proteus virtual COM port (o'zgartiring)
BAUDRATE = 9600

DEVICE_ID = b"YOUR_DEVICE_KEY"    # Manual Device ID (bytes yoki str bo'lsa moslang)
SECRET_KEY = b"YOUR_SECRET_KEY"   # Device Secret
# ------------------------------------------------

def logging_func():
    logging.basicConfig(
        datefmt="%H:%M:%S",
        format="%(asctime)s.%(msecs)03d %(message)s",
        level=logging.INFO,
    )

if __name__ == "__main__":
    logging_func()
    logger = logging.getLogger("serial-bridge")

    # ArduinoCloudClient yaratish (sizning kutubxona interfeysiga moslang)
    client = ArduinoCloudClient(device_id=DEVICE_ID, username=DEVICE_ID, password=SECRET_KEY)

    # Ro'yxatga olingan o'zgaruvchilarni saqlash uchun set
    registered_vars = set()

    # Serial portga ulanish
    try:
        ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)
        time.sleep(2)  # port stabil bo'lishi uchun
        logger.info(f"Serial port {SERIAL_PORT} ochildi, baud={BAUDRATE}")
    except Exception as e:
        logger.error(f"Serial portga ulanishda xato: {e}")
        raise SystemExit(1)

    # Clientni ishga tushirishdan oldin kerakli ro'yxatga olishlarni qilamiz.
    # Agar siz avvaldan ma'lum o'zgaruvchilarni bilsangiz, ularni shu yerda register qiling.
    # Misol: client.register("Temperature"); registered_vars.add("Temperature")

    # Start client (agar kutubxona talab qilsa)
    try:
        client.start()
        logger.info("ArduinoCloudClient ishga tushirildi")
    except Exception as e:
        # Ba'zi kutubxonalar register va start tartibini boshqacha talab qilishi mumkin.
        logger.warning(f"client.start() chaqirilganda ogohlantirish/xato: {e}")

    try:
        while True:
            try:
                raw = ser.readline().decode('utf-8', errors='ignore').strip()
            except Exception as e:
                logger.warning(f"Serial o'qishda xato: {e}")
                raw = ""

            if not raw:
                time.sleep(0.1)
                continue

            logger.info(f"Serial: {raw}")

            # Faraz: serial satr "key:value" formatida keladi
            if ':' not in raw:
                logger.warning("Serial satr formatiga mos emas (kutilgan: key:value). O'tkazib yuborildi.")
                continue

            key, val_str = raw.split(':', 1)
            key = key.strip()
            val_str = val_str.strip()

            # Agar kerak bo'lsa, qiymatni moslashtiring (float yoki int)
            try:
                if '.' in val_str:
                    value = float(val_str)
                else:
                    value = int(val_str)
            except ValueError:
                # Agar qiymat float/int ga aylanmasa, uni string sifatida yuborish mumkin
                value = val_str
                logger.info(f"Qiymat raqamga aylanmadi, string sifatida yuborilmoqda: {value}")

            # Agar o'zgaruvchi ro'yxatga olinmagan bo'lsa, register qiling
            if key not in registered_vars:
                try:
                    client.register(key)
                    registered_vars.add(key)
                    logger.info(f"{key} ro'yxatga olindi (registered).")
                except Exception as e:
                    logger.warning(f"{key} ni register qilishda xato: {e}")

            # Client obyekti orqali qiymatni yangilash
            try:
                client[key] = value
                logger.info(f"{key} = {value} yuborildi (client[{key}] = value).")
            except Exception as e:
                logger.error(f"{key} qiymatini client ga yozishda xato: {e}")

            # Agar kutubxona uchun qo'shimcha update/flush chaqiruvlari kerak bo'lsa, shu yerga qo'shing
            # Misol: client.update() yoki client.sync()

            time.sleep(0.5)

    except KeyboardInterrupt:
        logger.info("To'xtatildi (Ctrl+C)")

    finally:
        try:
            client.stop()
        except Exception:
            pass
        try:
            ser.close()
        except Exception:
            pass
        logger.info("Tugatildi")
