'''
Created on 28.03.2018

@author: D057816
'''

from MqttClient import MqttClient
from HmipClient import HmipClient
from threading import Thread
import logging
import logging.config

def setup_logger():
#    logging.basicConfig(level=logging.DEBUG)
    logging.config.fileConfig('logging.conf')
    global logger
    logger = logging.getLogger()
#    logging.config.fileConfig('logging.conf') #, defaults={'logfilename': '/var/log/rscHomematicIp/logging.log'})

def main():
    logger.error("Starting...")
    hmip_client = HmipClient()
    #hmip_client.readConfiguration()
    print(hmip_client)
    
    mqtt_client = MqttClient()
#    mqtt_client = None
    t = Thread(target=hmip_client.doLoop, args=(mqtt_client, ))
    t.start()    
    
    mqtt_client.startLoop(hmip_client)

#    mqtt_client.publish("cmdHomematicIp/testMessage", "This is a test message")
    
if __name__ == '__main__':
    setup_logger()
    main()