'''
Created on 29.03.2018

@author: D057816
'''

import asyncio
import json

import os

import configparser
import datetime
import json
import logging
from pprint import pprint
from homematicip.async.home import AsyncHome
from homematicip.base.base_connection import HmipConnectionError
from MqttClient import MqttClient
from HmipPublishHandler import HmipPublishHandler


class HmipClient:
    
    logger = logging.getLogger()
    
    def __init__(self):    
        self.readConfig()
        self.setup()
    
    def readConfig(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.hmip_authtoken = config['AUTH']['authtoken']
        self.hmip_accesspoint = config['AUTH']['accesspoint']
                
    def on_update_handler(self, data, event_type, obj):
        if obj:
            data['api_name'] = obj.__class__.__name__
        now = datetime.datetime.now()
        data['timestamp'] =now
        print(now.strftime('%Y-%m-%d_%H-%M-%S'))
        pprint(data)
        pprint(self.mqtt_client)
        label = data['label'].replace(" ", "_")
        sid = data['id'];
        topic = "msgHomematicIp/" + event_type + "/" + label;
        if data['api_name']:
            topic += "/" + data['api_name']
        payload = json.dumps(data)
        self.mqtt_client.publish(topic, payload)
        obj_type = ''
        if obj:
            obj_type = obj.__class__.__name__
        self.publishHandler.handle(self.mqtt_client, event_type, obj_type, label, data);
        # save the data.
        #_file_name = '{}_{}.json'.format(obj.__class__.__name__,
        #                                 datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        #_full_path = os.path.join('tests/json_data', _file_name)
        #with open(_full_path, 'w') as fl:
        #    json.dump(data, fl, indent=4)

    async def get_home(self, loop):
        self.logger.info("get_home")
        home = AsyncHome(loop)
        self.logger.debug("AuthToken="+self.hmip_authtoken)
        self.logger.debug("AccessPoint="+self.hmip_accesspoint)
        home.set_auth_token(self.hmip_authtoken)
        await home.init(self.hmip_accesspoint)
        self.logger.info("Home " + str(home))
        return home
    
    
    async def update_state(self, home):
        self.logger.info("update_state "+str(home))
        await home.get_current_state()
        self.logger.info("update_start success")
        for d in home.devices:
            print('{} {} {}'.format(d.id, d.label, str(d)))
        for d in home.groups:
            print('{} {} {}'.format(d.id, d.label, str(d)))
    
    
    async def wait_for_ws_incoming(self, home):
        await home.get_current_state()
        for d in home.devices:
            d.on_update(self.on_update_handler)
        for d in home.groups:
            d.on_update(self.on_update_handler)
        reader = await home.enable_events()
        await reader
    
    def readConfiguration(self):
        self.jsonConf = self.home.download_configuration()
        
        
    def setup(self):
        self.loop = asyncio.get_event_loop()
        self.home = None
        try:
            self.home = self.loop.run_until_complete(self.get_home(self.loop))
            self.readConfiguration()
        except HmipConnectionError:
            print("Problem connecting [1]")
        if self.home:   
            try:
                self.loop.run_until_complete(self.update_state(self.home))
            except HmipConnectionError:
                print("Problem connecting [2]")
#        loop.close()
#        self.doLoop()
        

    def doLoop(self, mqttClient):
        self.mqtt_client = mqttClient
#        self.publishHandler = HmipPublishHandler(mqttClient)
        print("HomematicIp Loop Start")
        #loop = asyncio.get_event_loop()
        try:
            self.loop.run_until_complete(self.wait_for_ws_incoming(self.home))
        except HmipConnectionError:
            print("Problem connecting [3]")
        except KeyboardInterrupt:
            self.loop.run_until_complete(self.home.close_websocket_connection())
        print("HomematicIp Loop End")
