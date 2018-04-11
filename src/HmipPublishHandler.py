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
    
    ThermometerItems = [
            { 'key': 'humidity',                'label': 'Humidity' },  
            { 'key': 'actualTemperature',       'label': 'ActualTemperature' },  
            { 'key': 'lowBat',                  'label': 'LowBat' }  
        ]
    
    ShutterContactItems = [
            { 'key': 'windowState',             'label': 'WindowState' },  # OPEN, CLOSED
            { 'key': 'lowBat',                  'label': 'LowBat' }  
        ]
    
    def __init__(self, mqtt_client): 
        self.mqttClient = mqtt_client
    
    def publishMqtt(self, topic, payload):
        self.logger.debug("publish -> topic <%s>" % topic)
        self.mqttClient.publish(topic, payload)
        
    def publishPlain(self, event_type, name, key, value):
        topic = self.topicMessage + "plain/" + name + '/' + key;
        payload = value
        self.publishMqtt(topic, payload)

    def handle(self, event_type, obj_type, label, data):
        if self.isHeating(obj_type, data):
            self.handleAsHeatingObj(event_type, obj_type, label, data)
        elif self.isShutter(obj_type, data):
            self.handleAsShutterObj(event_type, obj_type, label, data)
        elif self.isThermometer(obj_type, data):
            self.handleAsThermometerObj(event_type, obj_type, label, data)
        elif self.isShutterContact(obj_type, data):
            self.handleAsShutterContactObj(event_type, obj_type, label, data)
        topic = self.topicMessage + event_type + "/" + obj_type + '/' + label;
        payload = json.dumps(data)
        self.publishMqtt(topic, payload)
        
    def handleAsShutterContactObj(self, event_type, obj_type, label, data):
        topic1 = self.topicMessage + label + '/'
        for item in HmipPublishHandler.ShutterContactItems: 
            if item['key'] in data:
                subtopic = item['label']
                topic = topic1 + subtopic
                payload = data[item['key']]
                self.publishPlain(event_type, label, subtopic, payload)
            if 'functionalChannels' in data:
                for idx in data['functionalChannels']:
                    if item['key'] in data['functionalChannels'][idx]:
                        subtopic = item['label']
                        topic = topic1 + subtopic
                        payload = data['functionalChannels'][idx][item['key']]
                        self.publishPlain(event_type, label, subtopic, payload)

    def handleAsThermometerObj(self, event_type, obj_type, label, data):
        topic1 = self.topicMessage + label + '/'
        for item in HmipPublishHandler.ThermometerItems: 
            if item['key'] in data:
                subtopic = item['label']
                topic = topic1 + subtopic
                payload = data[item['key']]
                self.publishPlain(event_type, label, subtopic, payload)
            if 'functionalChannels' in data:
                for idx in data['functionalChannels']:
                    if item['key'] in data['functionalChannels'][idx]:
                        subtopic = item['label']
                        topic = topic1 + subtopic
                        payload = data['functionalChannels'][idx][item['key']]
                        self.publishPlain(event_type, label, subtopic, payload)

    def handleAsHeatingObj(self, event_type, obj_type, label, data):
        topic1 = self.topicMessage + label + '/'
        for item in HmipPublishHandler.HeatingItems: 
            if item['key'] in data:
                subtopic = item['label']
                topic = topic1 + subtopic
                payload = data[item['key']]
                self.publishPlain(event_type, label, subtopic, payload)
            if 'functionalChannels' in data:
                for idx in data['functionalChannels']:
                    if item['key'] in data['functionalChannels'][idx]:
                        subtopic = item['label']
                        topic = topic1 + subtopic
                        payload = data['functionalChannels'][idx][item['key']]
                        self.publishPlain(event_type, label, subtopic, payload)
                    
    def handleAsShutterObj(self, event_type, obj_type, label, data):
        topic1 = self.topicMessage + label + '/'
        for item in HmipPublishHandler.ShutterItems: 
            if item['key'] in data:
                subtopic = item['label']
                topic = topic1 + subtopic
                payload = data[item['key']]
                self.publishPlain(event_type, label, subtopic, payload)
            if 'functionalChannels' in data:
                for idx in data['functionalChannels']:
                    if item['key'] in data['functionalChannels'][idx]:
                        subtopic = item['label']
                        topic = topic1 + subtopic
                        payload = data['functionalChannels'][idx][item['key']]
                        self.publishPlain(event_type, label, subtopic, payload)
                    
    def isHeating(self, obj_type, data):
        if data and data['type'] == "HEATING_THERMOSTAT":
            return True
        if data and data['type'] == "WALL_MOUNTED_THERMOSTAT_PRO":
            return True
        return False
    
    def isShutter(self, obj_type, data):
        if data and data['type'] == "BRAND_SHUTTER":
            return True
        return False
    
    def isThermometer(self, obj_type, data):
        if data and data['type'] == "TEMPERATURE_HUMIDITY_SENSOR_OUTDOOR":
            return True
        return False
    
    def isShutterContact(self, obj_type, data):
        if data and data['type'] == "SHUTTER_CONTACT_INVISIBLE":
            return True
        return False    