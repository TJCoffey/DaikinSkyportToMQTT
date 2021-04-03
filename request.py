import logging
import os
from datetime import timedelta
import paho.mqtt.publish as publish
import json
import six
import crython

from daikinskyport import DaikinSkyport

with open('mapping.json') as f:
  mapping = json.load(f)

with open('config.json') as f:
    creds = json.load(f)
skyport = DaikinSkyport(None, creds['email'], creds['password'])

@crython.job(second=range(0, 60, 30))
def doUpdate():
    skyport.update()
    #print(skyport.thermostatlist)
    for thermostat in skyport.thermostatlist: #should just be the one
        thermoData = skyport.get_thermostat_info(thermostat['id'])
        #print(thermoData)

        for mapKey in mapping.keys():
            if mapKey in thermoData:
                #print(mapKey + " : " + mapping[mapKey] + " : " + str(thermoData[mapKey]))
                publish.single(mapping[mapKey], thermoData[mapKey], hostname=creds['mqttIP'])
        

if __name__ == '__main__':
    crython.start()
    crython.join()  ## This will block
