'''
Created on 25.03.2018

@author: D057816
'''


import paho.mqtt.client as mqtt


class MqttClient:
    
    topic = 'cmdHomematicIp/#'
    
    def __init__(self):    
        self.mqtt_broker = "192.168.178.42"
        self.mqtt_port = 1883
        self.setup()
    
    def on_publish(self, client, userdata, result):             #create function for callback
        print("data published \n")
        pass
    
    def on_connect(self, client, userdata, flags, rc):
        print("MQTT connected\n")
        client.subscribe(MqttClient.topic)
        client.publish("cmdHomematicIp/testMessage", "This is a test message")
 
    
    def on_message(self, client, userdata, message):
        print("message received " ,str(message.payload.decode("utf-8")))
        print("message topic=",message.topic)
        print("message qos=",message.qos)
        print("message retain flag=",message.retain)
    
    def setup(self): 
        self.mqtt_client= mqtt.Client("rscHomematicIP")         #create client object
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
        print("MQTT publish: topic=" + topic)
        ret = self.mqtt_client.publish(topic, payload)          #publish
        
    def startLoop(self, hmipClient):
        self.hmpipClient = hmipClient
 #       self.mqtt_client.loop_start()
        print("MQTT Loop Start")
        self.mqtt_client.loop_forever()
        print("MQTT Loop End")