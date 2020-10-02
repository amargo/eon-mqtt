# eon-mqtt
Magyar E.ON távleolvasási portálon keresztül jövő adatokat lehet MQTT-n tovább küldeni
Szabadon tovább fejleszthető, 1-2 óra alatt készült el ezért nagy hibakezelések és szofisztikált feladatok megoldására nem alkalmas.
Jelenleg a json responsból is kötötten szedi ki az adatokat:
https://github.com/amargo/eon-mqtt/blob/73a4605514c17313b990f830f92a71b1bc6968b2/read_eon_180_280.py#L111-L116

# Előfeltételek
Olyan GSM-es óra, amit küldi az adatokat a szolgáltató felé.
E.ON távleolvasási portálján érvényes regisztráció: https://energia.eon-hungaria.hu/W1000
Érvényes POD elérés után egy munkaterületet kell létrehozni:
<p align="center">    
        <img src="https://github.com/amargo/eon-mqtt/raw/master/img/eon-workarea.PNG" alt="eon-mqtt">
    <br>
</p>

Továbbá két Id-t kellett még megtudnom ezeket postman-os vizsgálatok során vettem észre, a reportId és a hyphen (ami nem tudom mi célt szolgál), de ezeket is át kell adni.
<p align="center">    
        <img src="https://github.com/amargo/eon-mqtt/raw/master/img/E.ON.PNG" alt="eon-mqtt">
    <br>
</p>

# Installation

1.Ezeket a csomagokat kell tepeíteni:
    
    sudo pip3 install paho-mqtt
    sudo pip3 install bs4

2.Kód klónozása:

    git clone https://github.com/amargo/eon-mqtt.git
    cd eon-mqtt

3.crontab feladatüzemezés hozzáadása. Mindennap 5 órakor fog lefutni:

    crontab -e
	# Add row
	0 5 * * * /usr/bin/python3 <path to eon-mqtt>/read_eon_180_280.py >> <path to eon-mqtt>/eon.log 2>&1  

4.Az `mqtt.ini.sample` kell át nevezni az `mqtt.ini`-re és beállítani az MQTT borker elérését `mqtt.ini`-ben.

5.Az `eon.ini.sample` kell át nevezni az `eon.ini`-re és beállítani az E.ON elérését `eon.ini`-ban:

    [MeroOra]
    eon_url = https://energia.eon-hungaria.hu/W1000
    topic=sensors/eon
    availability_topic=sensors/eon/availability
    username = <felhasználói azonosítód>
    password = <felhasználói jelszavad>
    reportId = <reportId>
    hyphen = <->
    since = <Mikortól, ha üresen hagyod, akkor az előző napit szedi le>
    until = <Meddig, ha üresen hagyod, akkor az előző napit szedi le>
        
    etc...

MQTT Payload példa:

    {"import_time": "2020-10-01T00:00:00", "import_value": 89.586, "export_time": "2020-10-01T00:00:00", "export_value": 222.556}
    
Integrálva HA alá:
<p align="center">    
        <img src="https://github.com/amargo/eon-mqtt/raw/master/img/mqtt_eon.PNG" alt="eon-mqtt">
    <br>
</p>

