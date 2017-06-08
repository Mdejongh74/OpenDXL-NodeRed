# OpenDXL-NodeRed Bridge

## Introduction
This project focus around real-time bi-directional data sharing **(bridging)** between McAfee DXL fabric and 3rd party data networks.

## Motivation
- Enable OpenDXL community to quickly create new integration use cases 
- Excel integration-adoption of OpenDXL technology.
- Create easy to use data bridging platform

## Getting Started (Bridge Service)
- McAfee OpenDXL wrapper service (py client) is responsible for securely collecting and forwarding data from and to McAfee Data Exchange layer (DXL)
- A flow based programming tool (Node-Red) enables easy wiring (coding) of 3rd party data source feeds (hardware devices, APIs, data sets and online data services) and orchestrate data traffic to and from McAfee DXL OpenDXL wrapper

![]({{site.baseurl}}/![image](https://user-images.githubusercontent.com/23244127/26917625-4a9a79a6-4c2f-11e7-90f7-cb3acdb837d2.png))

## Built With
- [CentOS Minimal](https://wiki.centos.org/Download) release v7:  free and open source Linux computing platform
- [Mosquito](https://mosquitto.org/download/) MQTT Message Broker release v1.4: Open source (EPL/EDL licensed) message broker that implements the MQTT protocol versions 3.1 and 3.1.1
- Eclipse [Paho](https://pypi.python.org/pypi/paho-mqtt/1.1) MQTT python client v1.1: Linux client class library which enable applications to connect to an MQTT broker to publish messages, and to subscribe to topics and receive published messages
- [Node-RED](http://nodered.org/) version 0.16.2(npm): Flow based programming tool for wiring together hardware devices, APIs and online data services
McAfee [OpenDXL](https://www.mcafee.com/us/developers/open-dxl/index.aspx) python Client


## Installation Bride Service
### Mosquitto MQTT Broker, Paho MQTT Client & Node-RED framework

1.Installing Mosquitto Broker & paho mqtt client from Package in CentOS 7:

```
$ sudo yum install epel-release
$ sudo yum -y install mosquitto
$ pip install paho-mqtt
```

2.Installing Node-RED in CentOS 7:

```
$ sudo yum install nodejs
$ sudo npm install -g --unsafe-perm node-red
```


### McAfee OpenDXL Client

Installation & Configuration MFE OpenDXL Client in CentOS 7:
1. Python SDK Installation [link](https://opendxl.github.io/opendxl-client-python/pydoc/installation.html)
2. Certificate Files Creation [link](https://opendxl.github.io/opendxl-client-python/pydoc/certcreation.html)
3. ePO Certificate Authority (CA) Import [link](https://opendxl.github.io/opendxl-client-python/pydoc/epocaimport.html)
4. ePO Broker Certificates Export [link](https://opendxl.github.io/opendxl-client-python/pydoc/epobrokercertsexport.html)
5. Edit MFE dxlclient.conf File [link](https://opendxl.github.io/opendxl-client-python/pydoc/sampleconfig.html)

## Running Bridge Service
### install Python3-function within Node-RED framework

```
$ npm install -g node-red-contrib-python3-function
```

### Create NodeRed-OpenDXL Publisher Node
1. Browse to URL Node-Red Admin UI **(Port:1880)**
2. Drop new **Python3 function** into dashboard flow and insert below Node code :

**_python code:_**

  ```python
import os
import sys
from dxlclient.client import DxlClient
from dxlclient.client_config import DxlClientConfig
from dxlclient.message import Event
EVENT_TOPIC = str(msg['topic']).encode()
CONFIG_FILE = "/var/McAfee/opendxl/examples/dxlclient.config"
config = DxlClientConfig.create_dxl_config_from_file(CONFIG_FILE)
with DxlClient(config) as client:
    client.connect()
    event = Event(EVENT_TOPIC)
    event.payload = str(msg['payload']).encode()
    client.send_event(event)
    return msg
```

## Start-up McAfee OpenDXL Bridge Service
In order to use the data bridge (wrapper) service, run OpenDXL_Bridge_Service.py script on the CentOS system:

$ python OpenDXL_Bridge_Service.py

## OpenDXL Bridge Service Output
After starting the python script and sucessfully setting-up the Node-Red framework below screen output will be displayed:

``` 
Received DXL Topic: /mcafee/event/dxl/brokerregistry/topicadded

Send MQTT Payload: {“topic”:#”}
```
