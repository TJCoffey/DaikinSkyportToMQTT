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

@crython.job(second=0)
def doUpdate():
    skyport.update()
    #print(skyport.thermostatlist)
    for thermostat in skyport.thermostatlist: #should just be the one
        thermoData = skyport.get_thermostat_info(thermostat['id'])

        #Just dump everything into the database except all the P1P2 and S21 that are empty on my system
        for key in thermoData:
            if key[:4] != "P1P2" and key[:3] != "S21" and key[:8] != "aqIndoor":
                #print(key + " : " + str(thermoData[key]))
                publish.single("home/testDump/" + key, thermoData[key], hostname=creds['mqttIP'])
        

if __name__ == '__main__':
    crython.start()
    crython.join()  ## This will block
