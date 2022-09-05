#!/usr/bin/python


DOCUMENTATION = '''
---

'''

EXAMPLES = '''
# Pass in a test txt file


'''

RETURN = '''

'''

from bs4 import BeautifulSoup
import paho.mqtt.publish as publish
import requests
import configparser
import os
import json
from datetime import datetime, timedelta

result = dict(message='')
def run_module():
    workdir = os.path.dirname(os.path.realpath(__file__))
    config = configparser.ConfigParser()
    config.read("{0}/eon.ini".format(workdir))
    mqtt_broker_cfg = init_mqtt(workdir)

    areas = config.sections()
    for area in areas:
        read_data(config, area, mqtt_broker_cfg)


def get_verificationtoken(content):
    try:
        toke = content.find('input', {'name': '__RequestVerificationToken'})
        return toke.get('value')
    except Exception as ex:
        module.fail_json(msg="Unable to get verification token." + str(ex) + ", content: " + str(content))

def init_mqtt(workdir):
    # Init MQTT
    mqtt_config = configparser.ConfigParser()
    mqtt_config.read("{0}/mqtt.ini".format(workdir))
    return mqtt_config["broker"]

def send_json(mqtt_broker_cfg, messages):
    try:
        auth = None
        mqtt_username = mqtt_broker_cfg.get("username")
        mqtt_password = mqtt_broker_cfg.get("password")

        if mqtt_username:
            auth = {"username": mqtt_username, "password": mqtt_password}

        publish.multiple(messages, hostname=mqtt_broker_cfg.get("host"), port=mqtt_broker_cfg.getint("port"), client_id=mqtt_broker_cfg.get("client"), auth=auth)
    except Exception as ex:
        print(datetime.now(), "Error publishing to MQTT: {0}".format(str(ex)))

def read_data(config, area, mqtt_broker_cfg):
    account_url = config[area].get('eon_url') + "/Account/Login"
    profile_data_url = config[area].get('eon_url') + "/ProfileData/ProfileData"
    username = config[area].get('username')
    password = config[area].get('password')
    messages = []

    try:
        session = requests.Session()
        content = session.get(account_url)
        index_content = BeautifulSoup(content.content, "html.parser")
        request_verification_token = get_verificationtoken(index_content)

        payload = {
            "UserName": username,
            "Password": password,
            "__RequestVerificationToken": request_verification_token
        }

        header = {"Content-Type": "application/x-www-form-urlencoded"}
        content = session.post(account_url, data=payload, headers=header)
        # print(session.cookies.get_dict())

        reportId = config[area].get('reportId')
        since = config[area].get('since')
        until = config[area].get('until')
        hyphen = config[area].get('hyphen')

        if not since:
            since = (datetime.now() + timedelta(days=-2)).strftime('%Y-%m-%d')
        if not until:
            until = (datetime.now() + timedelta(days=-1)).strftime('%Y-%m-%d')

        params = {
            "page": 1,
            "perPage": 2,
            "reportId": reportId,
            "since": since,
            "until": until,
            "-": hyphen
        }
        data_content = session.get(profile_data_url, params=params)
        jsonResponse = data_content.json()
        print(datetime.now(), jsonResponse)
        print(datetime.now(), area, " : ", jsonResponse)

        data = json.dumps({
            "import_time": jsonResponse[0]['data'][0]['time'],
            "import_value": jsonResponse[0]['data'][0]['value'],
            "export_time": jsonResponse[1]['data'][0]['time'],
            "export_value": jsonResponse[1]['data'][0]['value']
        })

        messages.append({'topic': config[area].get("topic"), 'payload': data , 'retain': config[area].getboolean("retain", False)})
        availability = 'Online'
    except Exception as ex:
        availability = 'Offline'
        print(datetime.now(), "Error retrive data from {0}.".format(str(ex)))
    finally:
        messages.append({'topic': config[area].get("availability_topic"), 'payload': availability, 'retain': config[area].getboolean("retain", False)})

    send_json(mqtt_broker_cfg, messages)

def main():
    run_module()


if __name__ == '__main__':
    main()
