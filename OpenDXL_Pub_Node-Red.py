import os
import sys

from dxlclient.client import DxlClient
from dxlclient.client_config import DxlClientConfig
from dxlclient.message import Event

EVENT_TOPIC = str(msg['topic']).encode()
CONFIG_FILE = "../dxlclient.config"
config = DxlClientConfig.create_dxl_config_from_file(CONFIG_FILE)

with DxlClient(config) as client:

    client.connect()
    event = Event(EVENT_TOPIC)
    event.payload = str(msg['payload']).encode()
    client.send_event(event)
    # node.send(msg)
    return msg