'''
Created on 25.03.2018

@author: D057816
'''


import paho.mqtt.client as mqtt
import logging
import configparser

logger = logging.getLogger('')

class MqttClient:
    
    SUBSCRIBE_TOPIC = "cmdHomematicIp/#"
    MQTT_CLIENT_ID = "rscHomematicIP"
    
    def __init__(self):    
        self.readConfig()
        self.setup()
    
    def readConfig(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.mqtt_broker = config['MQTT']['broker']
        self.mqtt_port = int(config['MQTT']['port'])
        logger.info("MQTT-Client: broker={} port={}".format(self.mqtt_broker, self.mqtt_port))
    
    def on_publish(self, client, userdata, result):             #create function for callback
        logger.debug("data published \n")
        pass
    
    def on_connect(self, client, userdata, flags, rc):
#        logger.debug("MQTT-Client connected\n")
        client.subscribe(self.SUBSCRIBE_TOPIC)
 #       client.publish("cmdHomematicIp/testMessage", "This is a test message")
 
    
    def on_message(self, client, userdata, message):
        logger.debug("message received " ,str(message.payload.decode("utf-8")))
        logger.debug("message topic=",message.topic)
        logger.debug("message qos=",message.qos)
        logger.debug("message retain flag=",message.retain)
    
    def setup(self): 
        self.mqtt_client= mqtt.Client(self.MQTT_CLIENT_ID)         #create client object
        self.mqtt_client.on_publish = self.on_publish           #assign function to callback
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message

        self.mqtt_client.connect(self.mqtt_broker, self.mqtt_port)        #establish connection
        
  #      self.mqtt_client.loop_start()                           #start the loop
#        Event Connection acknowledged Triggers the on_connect callback
#Event Disconnection acknowledged Triggers the on_disconnect callback
#Event Subscription acknowledged Triggers the  on_subscribe callback
#Event Un-subscription acknowledged Triggers the  on_unsubscribe callback
#Event Publish acknowledged Triggers the on_publish callback
#Event Message Received Triggers the on_message callback
#Event Log information available Triggers the on_log callback



    def publish(self, topic, payload):
        logger.debug("MQTT publish: topic=" + topic)
        ret = self.mqtt_client.publish(topic, payload)          #publish
        
    def startLoop(self, hmipClient):
        self.hmpipClient = hmipClient
 #       self.mqtt_client.loop_start()
        logger.debug("MQTT Loop Start")
        self.mqtt_client.loop_forever()
        logger.debug("MQTT Loop End")