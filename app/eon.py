#!/usr/bin/python

import os
import time
import json
import requests
import paho.mqtt.publish as publish

from datetime import datetime, timedelta
from pathlib import Path
from logger import log
from bs4 import BeautifulSoup
from mqtt_client import MqttClient

# from dotenv import load_dotenv


DOCUMENTATION = '''
---

'''

result = dict(message='')
__FILE = Path(__file__)
MQTT_CLIENT_ID = __FILE.name
MQTT_TOPIC = 'sensors/eon'
BASE_URL = 'https://energia.eon-hungaria.hu/W1000/'
ACCOUNT_URL = f'{BASE_URL}Account/Login'
PROFILE_DATA_URL = f'{BASE_URL}ProfileData/ProfileData'


def get_verificationtoken(content):
    try:
        token = content.find('input', {'name': '__RequestVerificationToken'})
        return token.get('value')
    except Exception as ex:
        raise Exception(
            f"Unable to get verification token from the following content: {content}")


def get_mqtt_client():
    mqtt_port = int(os.getenv('MQTT_PORT', 1883))
    mqtt_host = os.getenv('MQTT_HOST')
    mqtt_username = os.getenv('MQTT_USER')
    mqtt_password = os.getenv('MQTT_PASSWORD')

    mqtt_auth = {'username': mqtt_username,
                 'password': mqtt_password} if mqtt_username and mqtt_password else None
    mqtt_client = MqttClient(broker_host=mqtt_host,
                             broker_port=mqtt_port,
                             broker_auth=mqtt_auth)
    return mqtt_client


def main():
    # load_dotenv()
    eon_username = os.getenv('EON_USER')
    eon_password = os.getenv('EON_PASSWORD')

    session = requests.Session()
    # Suppress SSL certificate check!
    response = session.get(ACCOUNT_URL, verify=False)
    if response.status_code != 200:
        raise Exception(
            f"Failed to get access token, HTTP status code={response.status_code}")

    index_content = BeautifulSoup(response.content, "html.parser")

    log(f"Obtain an verification token")
    request_verification_token = get_verificationtoken(index_content)

    body_data = {
        "UserName": eon_username,
        "Password": eon_password,
        "__RequestVerificationToken": request_verification_token
    }

    header = {"Content-Type": "application/x-www-form-urlencoded"}
    log(f"Login into E.ON portal")
    response = session.post(ACCOUNT_URL, data=body_data,
                            headers=header, verify=False)  # Suppress SSL certificate check!
    if response.status_code != 200:
        raise Exception(
            f"Failed to login, HTTP status code={response.status_code}")

    reportId = os.getenv('EON_REPORT_ID')
    since = os.getenv('SINCE')
    until = os.getenv('UNTIL')
    hyphen = os.getenv('EON_HYPHEN')

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

    log(f"Retrieve data from E.ON")
    data_response = session.get(PROFILE_DATA_URL, params=params)
    if data_response.status_code != 200:
        raise Exception(
            f"Failed to retrieve data, HTTP status code={data_response.status_code}")
    json_eon_response = data_response.json()

    log(json_eon_response)

    data = json.dumps({
        "import_time": json_eon_response[0]['data'][0]['time'],
        "import_value": json_eon_response[0]['data'][0]['value'],
        "export_time": json_eon_response[1]['data'][0]['time'],
        "export_value": json_eon_response[1]['data'][0]['value']
    })
    messages = []
    mqtt_msg = {
        'topic': MQTT_TOPIC,
        'payload': data,
        'retain': True
    }
    messages.append(mqtt_msg)
    messages.append({'topic': f'{MQTT_TOPIC}/availability',
                    'payload': 'Online', 'retain': True})

    mqtt_client = get_mqtt_client()
    mqtt_client.publish_multiple(messages)
    log(messages)


if __name__ == '__main__':
    main()
