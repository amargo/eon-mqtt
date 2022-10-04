# eon-mqtt
Magyar E.ON távleolvasási portálon keresztül jövő adatokat lehet MQTT-n tovább küldeni
Szabadon tovább fejleszthető, 1-2 óra alatt készült el ezért nagy hibakezelések és szofisztikált feladatok megoldására nem alkalmas.

# Előfeltételek
Olyan GSM-es óra, amit küldi az adatokat a szolgáltató felé.
E.ON távleolvasási portálján érvényes regisztráció: https://energia.eon-hungaria.hu/W1000
Érvényes POD elérés után egy munkaterületet kell létrehozni, amin csak az 1.8.0 és 2.8.0 szerepeljen:
<p align="center">    
        <img src="https://github.com/amargo/eon-mqtt/raw/master/img/eon-workarea.PNG" alt="eon-mqtt">
    <br>
</p>

Továbbá két Id-t kellett még megtudnom ezeket postman-os vizsgálatok során vettem észre, a reportId és a hyphen (ami nem tudom mi célt szolgál), de ezeket is át kell adni.
<p align="center">    
        <img src="https://github.com/amargo/eon-mqtt/raw/master/img/E.ON.PNG" alt="eon-mqtt">
    <br>
</p>

Chrome-ban login előtt egy F12 és a Network tabon látszódni fog a reportId és a kötőjel (vagy aláhúzás). 
<p align="center">    
        <img src="https://github.com/amargo/eon-mqtt/raw/master/img/eon_reportId_hyphen.PNG" alt="eon-mqtt">
    <br>
</p>

# Docker
Elkészült egy dockerbe csomagolt változat is, amit jelenleg ütemezetten a leggyszerübb meghívni

1.Futtatás
```
docker run --env-file app/.env gszoboszlai/eon-mqtt
```

2.Ütemezés
Ezt egyszerüen már crontab-ba is be lehet rakni. Ez az ütemező bekerül későbbiekben az image-be is majd.

# Script használata

1.Kód klónozása:

    git clone https://github.com/amargo/eon-mqtt.git
    cd eon-mqtt

2.Ezeket a csomagokat kell tepeíteni:
    
    pip install -r requirements.txt

3.ENV használata
A legegyszerübb felrakni a dotenv csomagot és abból használni a fájlt.

MQTT Payload példa:

    {"import_time": "2020-10-01T00:00:00", "import_value": 89.586, "export_time": "2020-10-01T00:00:00", "export_value": 222.556}

# Beállítások:
Legegyszerübb egy .env fájlt használni, ehhez létre kell hozni pl egy app mappában:
```
EON_USER=<felhasználói azonosítód>
EON_PASSWORD=<felhasználói jelszavad>
EON_REPORT_ID=<reportId>
EON_HYPHEN=<->

MQTT_HOST=<mqtt host>
MQTT_USER=<felhasználói azonosítód>
MQTT_PASSWORD=<felhasználói jelszavad>
MQTT_TOPIC=<oplionális paraméter>

TZ=Europe/Budapest
``` 

Integrálva HA alá:
<p align="center">    
        <img src="https://github.com/amargo/eon-mqtt/raw/master/img/mqtt_eon.PNG" alt="eon-mqtt">
    <br>
</p>
