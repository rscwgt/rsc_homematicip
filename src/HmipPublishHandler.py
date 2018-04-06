'''
Created on 05.04.2018

@author: D057816
'''

import json
import logging

class HmipPublishHandler:
    
    topicMessage = "msgHomematicIp/"
    logger = logging.getLogger()
    
    HeatingItems = [  
            { 'key': 'setPointTemperature',     'label': 'SetPointTemperature' },  
            { 'key': 'actualTemperature',       'label': 'ActualTemperature' },  
            { 'key': 'humidity',                'label': 'Humidity' },  
            { 'key': 'controlMode',             'label': 'ControlMode' },  
            { 'key': 'windowState',             'label': 'WindowState' },  
            { 'key': 'valvePostion',            'label': 'ValvePosition' },  
            { 'key': 'lowBat',                  'label': 'LowBat' }  
        ]
    
    ShutterItems = [
            { 'key': 'shutterLevel',            'label': 'ShutterLevel' },  
            { 'key': 'profileMode',             'label': 'ProfileMode' },  
            { 'key': 'userDesiredProfileMode',  'label': 'UserDesiredProfileMode' },  
            { 'key': 'lowBat',                  'label': 'LowBat' }  
        ]
    
    def __init__(self, mqtt_client): 
        self.mqttClient = mqtt_client
    
    def publishMqtt(self, topic, payload):
        self.logger.debug("publish -> topic <%s>" % topic)
        self.mqttClient.publish(topic, payload)
        
    def publishPlain(self, event_type, object, key, value):
        topic = self.topicMessage + "plain/" + object + '/' + key;
        payload = value
        self.publishMqtt(topic, payload)

    def handle(self, event_type, obj_type, label, data):
        if self.isHeating(obj_type):
            self.handleAsHeatingObj(event_type, obj_type, label, data)
            pass
        elif self.isShutter(obj_type):
            self.handleAsShutterObj(event_type, obj_type, label, data)
            pass
        topic = self.topicMessage + event_type + "/" + obj_type + '/' + label;
        payload = json.dumps(data)
        self.publishMqtt(topic, payload)
        
    def handleAsHeatingObj(self, event_type, obj_type, label, data):
#        topic1 = self.topicMessage + obj_type + '/' + label + '/'
        topic1 = self.topicMessage + label + '/'
        for item in HmipPublishHandler.HeatingItems: 
            if item['key'] in data:
                topic = topic1 + item['label']
                payload = data[item['key']]
                self.publishMqtt(topic, payload)
            if 'functionalChannels' in data:
                for idx in data['functionalChannels']:
                    if item['key'] in data['functionalChannels'][idx]:
                        topic = topic1 + item['label']
                        payload = data['functionalChannels'][idx][item['key']]
                        self.publishMqtt(topic, payload)
                    
    def handleAsShutterObj(self, event_type, obj_type, label, data):
#        topic1 = self.topicMessage + obj_type + '/' + label + '/'
        topic1 = self.topicMessage + label + '/'
        for item in HmipPublishHandler.ShutterItems: 
            if item['key'] in data:
                topic = topic1 + item['label']
                payload = data[item['key']]
                self.publishMqtt(topic, payload)
            if 'functionalChannels' in data:
                for idx in data['functionalChannels']:
                    if item['key'] in data['functionalChannels'][idx]:
                        topic = topic1 + item['label']
                        payload = data['functionalChannels'][idx][item['key']]
                        self.publishMqtt(topic, payload)
                    
    def isHeating(self, obj_type):
        if "AsyncHeatingThermostat".lower() == obj_type.lower():
            return True
        if "AsyncWallMountedThermostatPro".lower() == obj_type.lower():
            return True
        return False
    
    def isShutter(self, obj_type):
        if "AsyncFullFlushShutter".lower() == obj_type.lower():
            return True
        return False