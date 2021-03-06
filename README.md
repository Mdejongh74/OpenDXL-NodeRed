![mfe logo](https://user-images.githubusercontent.com/23244127/26923460-71d3b0e2-4c42-11e7-8d93-5955f0b090f4.png)

# McAfee OpenDXL Bridge
 
## Introduction
This project focus around real-time bi-directional data sharing **(bridging)** between [McAfee Data Exchange Layer](https://www.mcafee.com/uk/solutions/data-exchange-layer.aspx "MFE DXL") and 3rd party data networks.

## Motivation
- Enable [OpenDXL community](https://community.mcafee.com/community/business/dxl/overview) to quickly create new integration use cases 
- Excel integration-adoption of OpenDXL
- Create easy to use data bridging platform

## Getting Started

### Main Bridge Service components
- **McAfee OpenDXL wrapper** : McAfee python Client service, responsible for securely collecting and forwarding data from and to McAfee Data Exchange layer (DXL).
- **Node-RED** :  Flow based graphical programming tool, enables easy wiring (coding) of 3rd party data source feeds (hardware devices, APIs, data sets and online data services) and manages data traffic orchestration into McAfee Data Exchange Layer (DXL).

![Architecture](https://user-images.githubusercontent.com/23244127/26922925-edd8ad84-4c40-11e7-9a02-bd5167fca79c.png)

## Prerequisites
- [CentOS Minimal](https://wiki.centos.org/Download) release v7:  free and open source Linux computing platform
- [Mosquito](https://mosquitto.org/download/) MQTT Message Broker release v1.4: Open source (EPL/EDL licensed) message broker that implements the MQTT protocol versions 3.1 and 3.1.1
- Eclipse [Paho](https://pypi.python.org/pypi/paho-mqtt/1.1) MQTT python client v1.1: Linux client class library which enable applications to connect to an MQTT broker to publish messages, and to subscribe to topics and receive published messages
- [Node-RED](http://nodered.org/) version 0.16.2(npm): Flow based programming tool for wiring together hardware devices, APIs and online data services
- McAfee [OpenDXL](https://www.mcafee.com/us/developers/open-dxl/index.aspx) python Client
- McAfee Data Exchange Layer Broker v3.x: MFE DXL Fabric Message broker
- McAfee ePolicy Orchestrator v5.3: Single console for Endpoint Security Management

## Installing Bride Service
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
2. Drop new **Python3 function** into dashboard flow

![python3_nodered](https://user-images.githubusercontent.com/23244127/26923264-dbcc2674-4c41-11e7-883f-de070d8830a2.png)

3. Edit new NodeRed-OpenDXL Function Node in Dashboard Flow and enter below python code (additionaly see file **OpenDXL_Pub_Node-Red.py**):

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

![python3_Node Fuction setup](https://user-images.githubusercontent.com/23244127/26920997-fd1078e6-4c3a-11e7-9576-61ef36e3914d.png)

## Start-up OpenDXL Bridge Service
In order to use the data bridge (wrapper) service, run **OpenDXL_Bridge.py** script on the CentOS system:

$ python OpenDXL_Bridge.py

## OpenDXL Bridge Service Output
After starting the python script and sucessfully setting-up the Node-Red framework below screen output will be displayed:

``` 
Received DXL Topic: /mcafee/event/dxl/brokerregistry/topicadded

Send MQTT Payload: {“topic”:#”}
```

## Example Flows OpenDXL Briding in Node-Red

See below a snapshot of a couple of Use-cases to integrate 3rd party data using OpenDXL Bridge Service and Node-RED:

![example flows](https://user-images.githubusercontent.com/23244127/26924402-fcdfa4cc-4c45-11e7-9bd4-a6db04a766b7.png)

## Versioning

For the versions available, see the tags on this repository.

## Authors

**Martin de Jongh** - Project design & Bridge Service programmer  - [McAfee](https://www.mcafee.com/us/index.html)

## Acknowledgments

- [Martin Ohl](https://github.com/mohl1/) - Supporting developer OpenDXL-NodeRed wrapper code - **McAfee**
- [Chris Smith](https://github.com/chrissmith-mcafee)- Development team OpenDXL Client - **McAfee**
- Thomas Maxeiner - Project Coach - **McAfee**

