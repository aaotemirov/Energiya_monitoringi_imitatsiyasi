import serial
import time
import logging
import sys
import threading
from arduino_iot_cloud import ArduinoCloudClient

# ---------- Sozlamalar ----------
SERIAL_PORT = 'COM3'        # Siz ochgan port
BAUD = 9600

DEVICE_ID = "834c57a9-28e6-4f9b-9be3-1f5b09c0af7c"
SECRET_KEY = "6s7n3WCNNG9FRELlKIh?LzNQ3"
# --------------------------------

logging.basicConfig(datefmt="%H:%M:%S", format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger("ArduinoCloud")

# Serial portga ulanish
try:
    ser = serial.Serial(SERIAL_PORT, BAUD, timeout=1)
    logger.info(f"Serial port {SERIAL_PORT} muvaffaqiyatli ochildi.")
except Exception as e:
    logger.error(f"Serial portga ulanishda xato: {e}")
    sys.exit(1)

# Arduino Cloud mijozini yaratish
client = ArduinoCloudClient(device_id=DEVICE_ID, username=DEVICE_ID, password=SECRET_KEY)

# Platformadagi o'zgaruvchingiz
client.register("harorat", value=0.0)
client.register("namlik", value=0.0)
client.register("Markaziy_U", value=0.0)
client.register("DC_U", value=0.0)
client.register("DC_I", value=0.0)
client.register("DC_Pow", value=0.0)
client.register("AC_U", value=0.0)
client.register("AC_I", value=0.0)
client.register("AC_Pow", value=0.0)
client.register("QP_U", value=0.0)
client.register("QP_Yo", value=0.0)
client.register("QP_Ch", value=0.0)
client.register("DG_U", value=0.0)
client.register("DG_hajm", value=0.0)
client.register("AB_U", value=0.0)
client.register("AB_T", value=0.0)
client.register("AB_ZM", value=0.0)
client.register("sh_U", value=0.0)
client.register("sh_tez", value=0.0)
client.register("sh_yun", value="N/A")

client.register("status_M", value=False)
client.register("status_SH", value=False)
client.register("status_QP", value=False)
client.register("status_DG", value=False)
client.register("status_AB", value=False)

def on_connect(client):
    logger.info("Arduino IoT Cloud platformasiga muvaffaqiyatli ulandi!")

client.on_connect = on_connect

# PROTEUS PORTINI O'QISH FUNKSIYASI
def read_proteus_serial():
    logger.info("Proteus portini o'qish oqimi ishga tushdi. Ma'lumotlar kutilmoqda...")

    DG_U =0.0
    Markaziy_U =0.0
    QP_U = 0.0
    sh_U = 0.0

    while True:
        try:
            if not ser.is_open:
                break
                
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                if line and ' = ' in line:
                    logger.info(f"Proteus'dan kelgan xabar: {line}")
                    k, v = line.split(' = ', 1)
                    qiymat_v = v.split(' ')[0]
                    qiymat = float(qiymat_v)

                    # Ma'lumotni bulutga yuborish
                    if k == "Muhit Harorati":
                            client["harorat"] = qiymat
                            logger.info(f"Bulutga yuborildi [Harorat]: {qiymat}°C")
                    elif k == "Muhit Namligi":
                                client["namlik"] = qiymat
                                logger.info(f"Bulutga yuborildi [Namlik]: {qiymat}%")
                    elif k == "U_Markaz":
                                    client["Markaziy_U"] = qiymat
                                    Markaziy_U = qiymat
                                    logger.info(f"Bulutga yuborildi [U_Markaziy]: {qiymat}V")
                    elif k == "Yuklama (DC)":
                                    client["DC_U"] = qiymat
                                    logger.info(f"Bulutga yuborildi [U_Yuklama(DC)]: {qiymat}V")
                    elif k == "Tok kuchi (DC)":
                                    client["DC_I"] = qiymat
                                    logger.info(f"Bulutga yuborildi [I_Yuklama(DC)]: {qiymat}A")
                    elif k == "Istemol quvvati (DC)":
                                    client["DC_Pow"] = qiymat
                                    logger.info(f"Bulutga yuborildi [Quvvat(DC)]: {qiymat}W")
                    elif k == "Yuklama (AC)":
                                    client["AC_U"] = qiymat
                                    logger.info(f"Bulutga yuborildi [U_Yuklama(AC)]: {qiymat}V")
                    elif k == "Tok kuchi (AC)":
                                    client["AC_I"] = qiymat
                                    logger.info(f"Bulutga yuborildi [I_Yuklama(AC)]: {qiymat}A")
                    elif k == "Istemol quvvati (AC)":
                                    client["AC_Pow"] = qiymat
                                    logger.info(f"Bulutga yuborildi [Quvvat(AC)]: {qiymat}W")                
                    elif k == "U_QP":
                                    client["QP_U"] = qiymat
                                    QP_U = qiymat
                                    logger.info(f"Bulutga yuborildi [U_quyosh]: {qiymat}V")
                    elif k == "Yoritilganlik":
                                    client["QP_Yo"] = qiymat
                                    logger.info(f"Bulutga yuborildi [Yoritilganlik]: {qiymat}LUX")
                    elif k == "Changlanganlik":
                                    client["QP_Ch"] = qiymat
                                    logger.info(f"Bulutga yuborildi [Yoritilganlik]: {qiymat}%")
                    elif k == "U_DG":
                                    client["DG_U"] = qiymat
                                    DG_U = qiymat
                                    logger.info(f"Bulutga yuborildi [DG_kuchlanish]: {qiymat}V")
                    elif k == "Dizel":
                                    client["DG_hajm"] = qiymat
                                    logger.info(f"Bulutga yuborildi [Dizel miqdori]: {qiymat}Litr")
                    elif k == "U_AB":
                                    client["AB_U"] = qiymat
                                    logger.info(f"Bulutga yuborildi [AB_kuchlanish]: {qiymat}V")
                    elif k == "AKB harorati":
                                    client["AB_T"] = qiymat
                                    logger.info(f"Bulutga yuborildi [AB_harorat]: {qiymat}°C")                
                    elif k == "AKB zaryad":
                                    client["AB_ZM"] = qiymat
                                    logger.info(f"Bulutga yuborildi [AB_zaryad]: {qiymat}%")                
                    elif k == "U_SH":
                                    client["sh_U"] = qiymat
                                    sh_U = qiymat
                                    logger.info(f"Bulutga yuborildi [U_Shamol]: {qiymat}V")
                    elif k == "Shamol tezligi ":
                                    client["sh_tez"] = qiymat
                                    logger.info(f"Bulutga yuborildi [Shamol_tezlik]: {qiymat}km/soat")                
                    elif k == "Shamol yo'nalishi":
                                    deg = float(qiymat)
                                    if (deg >= 337.5 or deg < 22.5):
                                        sh_matn = "Shimol (N)"
                                    elif (deg >= 22.5 and deg < 67.5):
                                        sh_matn = "Shimol-Sharq (NE)"
                                    elif (deg >= 67.5 and deg < 112.5):
                                        sh_matn = "Sharq (E)"
                                    elif (deg >= 112.5 and deg < 157.5):
                                        sh_matn = "Janub-Sharq (SE)"
                                    elif (deg >= 157.5 and deg < 202.5):
                                        sh_matn = "Janub (S)"
                                    elif (deg >= 202.5 and deg < 247.5):
                                        sh_matn = "Janub-G'arb (SW)"
                                    elif (deg >= 247.5 and deg < 292.5):
                                        sh_matn = "G'arb (W)"
                                    elif (deg >= 292.5 and deg < 337.5):
                                        sh_matn = "Shimol-G'arb (NW)"

                                    client["sh_yun"] = sh_matn
                                    logger.info(f"Bulutga yuborildi [deg]: {qiymat}Gradus")

            status_M = True if Markaziy_U > 46 and QP_U < 46 and sh_U < 46 else False
            status_SH = True if QP_U < 46 and sh_U > 45 else False
            status_QP = True if QP_U > 45 else False
            status_DG  = True if DG_U > 45 and Markaziy_U < 46 and QP_U < 46 and sh_U < 46 else False
            status_AB    = True if DG_U < 45 and Markaziy_U < 46 and QP_U < 46 and sh_U < 46 else False

            client["status_M"] = status_M
            client["status_SH"] = status_SH
            client["status_QP"] = status_QP
            client["status_DG"]  = status_DG
            client["status_AB"]    = status_AB
            
        except ValueError:
            logger.warning(f"Kelgan qiymatni songa o'girib bo'lmadi: {line}")
        except Exception as e:
            logger.error(f"Serial o'qishda ichki xato: {e}")
            break
        time.sleep(0.5)

# Proteus oqimini yaratish va ishga tushirish
serial_thread = threading.Thread(target=read_proteus_serial, daemon=True)
serial_thread.start()

# Arduino Cloud'ni fonda boshlash
logger.info("Bulutga ulanish jarayoni boshlandi...")
client.start()

# Asosiy dastur yopilib ketmasligi uchun cheksiz sikl
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    logger.info("Dastur foydalanuvchi tomonidan to'xtatildi.")
finally:
    client.stop()
    if ser.is_open:
        ser.close()
    logger.info("Serial port yopildi va dastur yakunlandi.")
