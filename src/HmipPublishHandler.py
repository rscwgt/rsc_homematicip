'''
Created on 05.04.2018

@author: D057816
'''

import json

class HmipPublishHandler:
    
    topicMessage = "msgHomematicIp/"
    
    def __init__(self, mqtt_client): 
        self.mqttClient = mqtt_client
    
    def publishPlain(self, event_type, object, key, value):
        topic = self.topicMessage + "plain/" + object + '/' + key;
        payload = value
        self.mqttClient.publish(topic, payload)

    def handle(self, event_type, obj_type, label, data):
        if self.isHeating(obj_type):
            self.handleAsHeatingObj(event_type, obj_type, label, data)
            pass
        topic = self.topicMessage + event_type + "/" + obj_type + '/' + label;
        payload = json.dumps(data)
        self.mqttClient.publish(topic, payload)
        
    def handleAsHeatingObj(self, event_type, obj_type, label, data):
        topic1 = self.topicMessage + obj_type + '/' + label + '/'
        if data['setPointTemperature']:
            topic = topic1 + 'SetPointTemperature'
            payload = data['setPointTemperature']
            self.mqttClient.publish(topic, payload)
    
    def isHeating(self, obj_type):
        if "AsyncHeatingThermostat".lower() == obj_type.lower():
            return True
        if "AsyncWallMountedThermostatPro".lower() == obj_type.lower():
            return True
        
        return False;