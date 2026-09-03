# Energiya Monitoring Tizimi — Imitatsiya, Ma’lumot Almashish va Boshqaruv

**Elektr energetika tizimlarini modellashtirish, simulyatsiya qilish va monitoring qilish uchun apparat-dasturiy platforma**

[![GitHub](https://img.shields.io/badge/GitHub-Repository-black?logo=github)](https://github.com/aaotemirov/Energiya_monitoringi_imitatsiyasi)
[![License](https://img.shields.io/badge/License-To%20be%20defined-lightgrey)](#litsenziya)

---

## 📌 Loyiha haqida

Ushbu repository elektr energetika tizimining alohida funksional qismlarini **imitatsiya qilish, elektron sxemalarni modellashtirish, mikrokontroller asosida boshqarish va ma’lumot almashish jarayonlarini tadqiq qilish** uchun ishlab chiqilgan apparat-dasturiy yechimni o‘z ichiga oladi.

Loyiha tarkibida **Proteus** muhitida ishlab chiqilgan elektron sxemalar, **Arduino Mega** mikrokontrolleriga tegishli dasturiy ta’minot, **Python** asosidagi Serial aloqa dasturlari hamda **MQTT** protokoli orqali ma’lumot almashish komponentlari mavjud.

Tizimning asosiy qismlari elektr energiyasini **uzatish, qabul qilish, o‘zgartirish, boshqarish va monitoring qilish** jarayonlarini yagona tajriba muhiti doirasida o‘rganish imkonini beradi.

---

## 🎯 Loyiha maqsadi

Loyihaning asosiy maqsadi elektr energetika tizimlarida qo‘llaniladigan apparat va kommunikatsiya komponentlarini real qurilmalarni ishga tushirishdan oldin **raqamli simulyatsiya va apparat-dasturiy integratsiya muhiti** orqali tadqiq qilishdan iborat.

Asosiy vazifalar:

* elektr energiyasini uzatish jarayonini modellashtirish;
* elektr energiyasini qabul qilish jarayonini modellashtirish;
* invertor qurilmasining ishlashini simulyatsiya qilish;
* Arduino Mega asosida boshqaruvni tashkil etish;
* Serial aloqa orqali ma’lumot almashish;
* MQTT protokoli orqali ma’lumotlarni uzatish;
* tizim komponentlarining o‘zaro integratsiyasini sinovdan o‘tkazish;
* turli konfiguratsiyalar va tajriba natijalarini saqlash.

---

## 🧩 Tizimning umumiy arxitekturasi

Loyihaning funksional tuzilmasi quyidagi ketma-ketlik asosida tashkil etilgan:

```text
                  ELEKTR ENERGIYA TIZIMI
                           │
             ┌─────────────┴─────────────┐
             │                           │
        UZATISH TIZIMI              INVERTOR
             │                           │
             └─────────────┬─────────────┘
                           │
                     QABUL TIZIMI
                           │
                       ARDUINO
                           │
                    SERIAL ALOQA
                           │
                         PYTHON
                           │
                         MQTT
                           │
                  MA’LUMOT ALMASHISH
                           │
                     MONITORING
```

Ushbu arxitektura elektr energetika obyektlarining fizik jarayonlarini elektron simulyatsiya, mikrokontroller va kommunikatsiya qatlamlari bilan birlashtirishga mo‘ljallangan.

---

# ⚡ Elektr energiyasini uzatish tizimi

`1. Uzatish/` katalogida elektr energiyasini uzatish jarayonining Proteus muhitidagi modellariga tegishli fayllar joylashgan.

### Asosiy loyihalar

* `Azizbek_Uzatish.pdsprj`
* `Simulyatsiya_1.1(Azizbek).pdsprj`
* `Azizbek_Uzatish.PDF`

Ushbu modul elektr energiyasini uzatish jarayonidagi elektron komponentlarning o‘zaro ishlashini simulyatsiya qilish uchun foydalaniladi.

---

# 📥 Elektr energiyasini qabul qilish tizimi

`2. Qabul/` katalogida elektr energiyasini qabul qilish va qayta ishlash qismiga tegishli loyihalar mavjud.

### Asosiy fayllar

* `Qabul_V2.pdsprj`
* `Qabul_V2.PDF`
* `ARDUINO_MEGA_1.HEX`

Arduino Mega uchun tayyorlangan `.HEX` fayl mikrokontroller asosidagi boshqaruv jarayonlarini simulyatsiya qilishda qo‘llaniladi.

---

# 🔄 Invertor

`Invertor/` katalogida invertor qurilmasining Proteus muhitidagi modeli joylashgan.

### Asosiy loyiha

```text
Invertor/Invertor.pdsprj
```

Ushbu modul elektr energiyasini o‘zgartirish bilan bog‘liq jarayonlarni elektron sxema asosida modellashtirish imkonini beradi.

---

# 📡 MQTT orqali ma’lumot almashish

`MQQT v2/` katalogi tizimdagi ma’lumotlarni kommunikatsiya qilish uchun ishlab chiqilgan MQTT komponentlarini o‘z ichiga oladi.

Asosiy Proteus loyihasi:

```text
MQQT v2/mqqt_v2.pdsprj
```

Ushbu katalogda Python asosidagi Serial aloqa dasturlarining bir nechta tajriba versiyalari ham mavjud:

```text
Serial_sent_v2.py
Serial_sent_v3.py
Serial_sent_v4.py
Serial_sent_v5.py
Serial_sent_v6.py
Serial_sent_v7.py
```

Bu versiyalar ishlab chiqish jarayonida ma’lumot uzatish mexanizmlarini sinash va takomillashtirish uchun foydalanilgan.

---

# 🖥️ Python va Serial aloqa

Python dasturlari kompyuter va mikrokontroller o‘rtasidagi Serial aloqa jarayonini tashkil qilishda ishlatiladi.

Asosiy dasturlardan biri:

```text
Serial_sent_v7.py
```

Serial aloqa quyidagi vazifalarni bajarish uchun mo‘ljallangan:

* ma’lumotlarni mikrokontrollerga yuborish;
* mikrokontrollerdan ma’lumotlarni qabul qilish;
* tizim komponentlari o‘rtasida kommunikatsiyani tashkil qilish;
* keyingi MQTT kommunikatsiyasi uchun ma’lumotlarni tayyorlash.

---

# 🔬 Proteus simulyatsiyasi

Loyihaning apparat qismi **Proteus Design Suite** muhitida modellashtirilgan.

Proteus orqali quyidagi jarayonlarni virtual muhitda tekshirish mumkin:

1. Elektr sxemalarining ishlashi;
2. komponentlarning o‘zaro bog‘lanishi;
3. Arduino Mega ishlashi;
4. elektr energiyasini uzatish va qabul qilish;
5. invertor ishlash jarayoni;
6. Serial kommunikatsiya;
7. tizimning turli konfiguratsiyalarini sinash.

Bu yondashuv real apparat prototipini yaratishdan oldin tizimning asosiy funksiyalarini virtual muhitda tekshirish imkonini beradi.

---

# 🧠 Apparat-dasturiy integratsiya

Loyiha uchta asosiy qatlamning integratsiyasiga asoslanadi:

| Qatlam                  | Texnologiya  | Vazifasi                               |
| ----------------------- | ------------ | -------------------------------------- |
| Elektron model          | Proteus      | Elektr sxemalarini simulyatsiya qilish |
| Boshqaruv               | Arduino Mega | Mikrokontroller asosidagi boshqaruv    |
| Dasturiy aloqa          | Python       | Serial kommunikatsiya                  |
| Tarmoq kommunikatsiyasi | MQTT         | Ma’lumot almashish                     |

---

# 📁 Repository tuzilishi

```text
Energiya_monitoringi_imitatsiyasi/
│
├── 1. Uzatish/
│   ├── Azizbek_Uzatish.pdsprj
│   ├── Simulyatsiya_1.1(Azizbek).pdsprj
│   ├── Azizbek_Uzatish.PDF
│   └── Project Backups/
│
├── 2. Qabul/
│   ├── Qabul_V2.pdsprj
│   ├── Qabul_V2.PDF
│   ├── ARDUINO_MEGA_1.HEX
│   └── Project Backups/
│
├── Invertor/
│   ├── Invertor.pdsprj
│   └── Project Backups/
│
├── MQQT v2/
│   ├── mqqt_v2.pdsprj
│   ├── Python to serial/
│   │   ├── Serial sent.py
│   │   ├── Serial_sent_v2.py
│   │   ├── Serial_sent_v3.py
│   │   ├── Serial_sent_v4.py
│   │   ├── Serial_sent_v5.py
│   │   ├── Serial_sent_v6.py
│   │   └── Serial_sent_v7.py
│   └── Project Backups/
│
├── Serial_sent_v7.py
│
└── rasm/
    └── Simulyatsiya rasmlari
```

---

# 🧪 Tajriba va simulyatsiya jarayoni

Loyiha bilan ishlashning umumiy ketma-ketligi:

```text
1. Proteus sxemasini ochish
          ↓
2. Elektr komponentlarini sozlash
          ↓
3. Arduino dasturini yuklash
          ↓
4. Simulyatsiyani ishga tushirish
          ↓
5. Serial ma’lumot almashinuvini tekshirish
          ↓
6. Python dasturini ishga tushirish
          ↓
7. MQTT kommunikatsiyasini tekshirish
          ↓
8. Natijalarni tahlil qilish
```

---

# 💻 Foydalanilgan texnologiyalar

* **Proteus Design Suite** — elektron sxemalarni loyihalash va simulyatsiya qilish;
* **Arduino Mega** — mikrokontroller asosidagi boshqaruv;
* **Python** — Serial aloqa va yordamchi dasturlar;
* **MQTT** — xabarlar asosidagi kommunikatsiya;
* **Serial Communication** — qurilmalar o‘rtasidagi ma’lumot almashish;
* **Git** — versiyalarni boshqarish;
* **GitHub** — dasturiy kod va loyiha fayllarini saqlash.

---

# 🔁 Reproduksiya

Tadqiqot natijalarini qayta ishlab ko‘rish uchun:

1. Repository'ni klonlash;
2. Tegishli Proteus loyihasini ochish;
3. Arduino Mega uchun `.HEX` faylni ulash;
4. Proteus simulyatsiyasini ishga tushirish;
5. Python Serial dasturini ishga tushirish;
6. MQTT kommunikatsiyasini sozlash;
7. natijalarni qayta tekshirish.

Repository:

`https://github.com/aaotemirov/Energiya_monitoringi_imitatsiyasi`

---

# 📚 Ilmiy foydalanish va iqtibos keltirish

Ushbu repository ilmiy maqolalar, konferensiya materiallari, bitiruv malakaviy ishlari, magistrlik dissertatsiyalari va boshqa ilmiy tadqiqotlarda loyiha manbasi sifatida keltirilishi mumkin.

## GitHub orqali iqtibos

**Temirov, A. (2026). Energiya Monitoring Tizimi — Imitatsiya, Ma’lumot Almashish va Boshqaruv. GitHub repository.**

> DOI mavjud bo‘lgandan keyin ushbu citation DOI bilan yangilanadi.

## BibTeX

```bibtex
@software{temirov2026energiya,
  author       = {Temirov, Azizbek},
  title        = {Energiya Monitoring Tizimi — Imitatsiya, Ma'lumot Almashish va Boshqaruv},
  year         = {2026},
  publisher    = {GitHub},
  url          = {https://github.com/aaotemirov/Energiya_monitoringi_imitatsiyasi}
}
```

## APA

```text
Temirov, A. (2026). Energiya Monitoring Tizimi — Imitatsiya, Ma’lumot Almashish va Boshqaruv [Computer software]. GitHub.
```

---

# 🏷️ DOI

Ushbu repository uchun DOI **Zenodo orqali arxivlangandan keyin** ushbu bo‘limga joylashtiriladi.

```text
DOI: [Zenodo tomonidan beriladigan DOI]
```

DOI olingandan keyin yuqoridagi GitHub citation, BibTeX va APA ma’lumotlari DOI bilan yangilanadi.

---

# 📌 Versiyalash

Ilmiy tadqiqotlarda natijalarning takrorlanishini ta’minlash uchun repository versiyalarini saqlash tavsiya etiladi.

Har bir muhim ilmiy yoki texnik o‘zgarish uchun Git tag yaratish mumkin:

```bash
git tag v1.0.0
git push origin v1.0.0
```

Masalan:

```text
v1.0.0 — Dastlabki barqaror versiya
v1.1.0 — MQTT kommunikatsiyasi
v1.2.0 — Serial aloqa takomillashtirilishi
v2.0.0 — Tizimning yangi konfiguratsiyasi
```

---

# 👤 Muallif

**Azizbek Temirov**

Elektr energetikasi, avtomatlashtirish, elektron tizimlar va energiya monitoringi yo‘nalishlarida tadqiqot va dasturiy-apparat tizimlarini ishlab chiqish.

---

# 📄 Litsenziya

Litsenziya turi repository egasi tomonidan belgilanadi.

Agar loyiha ochiq ilmiy dasturiy ta’minot sifatida tarqatiladigan bo‘lsa, MIT, Apache-2.0 yoki boshqa mos litsenziyalardan birini tanlash mumkin.

---

# 📖 Citation

Agar ushbu repository'dan ilmiy tadqiqotda foydalanilgan bo‘lsa, repository'ga citation berish tavsiya etiladi.

**DOI mavjud bo‘lgandan keyingi asosiy citation shakli:**

```text
Temirov, A. (2026). Energiya Monitoring Tizimi — Imitatsiya, Ma’lumot Almashish va Boshqaruv. DOI: [DOI]
```

---

## 🔗 Repository

[Energiya_monitoringi_imitatsiyasi — GitHub](https://github.com/aaotemirov/Energiya_monitoringi_imitatsiyasi?utm_source=chatgpt.com)

---

**Loyiha holati:** Faol ishlab chiqish / tadqiqot va simulyatsiya bosqichi.
