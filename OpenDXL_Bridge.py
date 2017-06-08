# Copyright (c) 2017 Martin de Jongh <martin_dejongh@mcafee.com>
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Distribution License v1.0
# which accompanies this distribution. 
#
# The Eclipse Distribution License is available at 
#   http://www.eclipse.org/org/documents/edl-v10.php.
#
# Contributors:
#    Martin de Jongh - initial implementation

# Below python script forwards McAfee DXL messages to Node-RED and MQTT fabric (1-to-1).
 
import logging
import os
import sys
import time

from dxlclient.callbacks import EventCallback
from dxlclient.client import DxlClient
from dxlclient.client_config import DxlClientConfig
import paho.mqtt.client as mqtt

# Import common OpenDXL logging and configuration
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from common import *

# Configure local logger
logging.getLogger().setLevel(logging.ERROR)
logger = logging.getLogger(__name__)

# Create DXL configuration from file
config = DxlClientConfig.create_dxl_config_from_file(CONFIG_FILE)

# Connect to (localhost) MQTT Broker using paho MQTT client
mqtt_client = mqtt.Client(
    client_id="", clean_session=True, userdata=None, protocol=mqtt.MQTTv31)
mqtt_client.connect("localhost", 1883)

# Create OpenDXL client and connect to MFE DXL fabric
with DxlClient(config) as client:
    # Connect to the DXL fabric
    client.connect()

    # Create OpenDXL event listener and display received MFE DXL Topic
    class MyEventCallback(EventCallback):
        def on_event(self, event):
            try:
                print "Received DXL Topic: " + event.destination_topic
                pl = str(event.payload.decode("UTF-8")).rstrip("\0")
                
                # Publish MFE DXL Data using Paho MQTT client to MQTT fabric
                mqtt_client.publish(topic=event.destination_topic, payload=pl, qos=0)
		print "Send MQTT Payload: " + pl
		mqtt_client.loop_start()

            except Exception as e:
                print e

    # Register the callback with the OpenDXL client
    client.add_event_callback('#', MyEventCallback(), subscribe_to_topic=False)
    
    # If nessesary you can subscripe, listen & forward induvidual MFE DXL Topics instead of everything published (#)
    client.subscribe("#")
    # Optional: Change client.subscribe ("topic") if you want to listen to specific MFE DXL topics/messages, see examples below..
    #client.subscribe("/mcafee/event/atd/#")
    #client.subscribe("/mcafee/event/tie/#")
    #client.subscribe("/mcafee/event/epo/#")

    # Wait forever
    while True:
        time.sleep(60)