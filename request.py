import logging
import os
from datetime import timedelta
import paho.mqtt.publish as publish
import json
import six
import crython

from daikinskyport import DaikinSkyport

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

        #Just dump everything into the database
        for param in thermoData:
            #print(mapKey + " : " + mapping[mapKey] + " : " + str(thermoData[mapKey]))
            print("/home/testDump/" + param + " : " thermoData[param])
            publish.single("/home/testDump/" + param, thermoData[param], hostname=creds['mqttIP'])
        

if __name__ == '__main__':
    crython.start()
    crython.join()  ## This will block
