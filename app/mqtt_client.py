# -*- coding: utf-8 -*-
"""
@author: amargo
"""

import paho.mqtt.publish as publish

from pathlib import Path
from typing import Any, Dict, List, Optional

__FILE = Path(__file__)
MQTT_CLIENT_ID = __FILE.name


class MqttClient:
    def __init__(self, broker_host: str, broker_port: int, broker_auth: Optional[dict] = None):
        self.__connection_options = {
            'hostname': broker_host,
            'port': broker_port,
            'auth': broker_auth,
            'client_id': MQTT_CLIENT_ID
        }

    def publish_multiple(self, payloads: List[Dict[str, Any]], **kwargs) -> None:
        publish.multiple(payloads, **self.__connection_options, **kwargs)

    def publish_single(self, topic: str, payload: str, **kwargs) -> None:
        publish.single(topic, payload, **self.__connection_options, **kwargs)
