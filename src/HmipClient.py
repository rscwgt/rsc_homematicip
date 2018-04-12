'''
Created on 29.03.2018

@author: D057816
'''

import asyncio
import json

import os

import configparser
import datetime
import time
import json
import logging
import pprint
from homematicip.home import Home
from homematicip.async.home import AsyncHome
from homematicip.base.base_connection import HmipConnectionError
from MqttClient import MqttClient
from HmipPublishHandler import HmipPublishHandler

#import config

LOGGER = logging.getLogger()
#LOGGER = logging.getLogger(__name__)

class HmipClient:
    
    def __init__(self):  
        LOGGER.error("HmipClient")  
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
        now = time.time()
        data['timestamp'] = now
        LOGGER.debug(datetime.datetime.fromtimestamp(now).strftime('%Y-%m-%d_%H-%M-%S'))
        LOGGER.debug(pprint.pformat(data))
        label = data['label'].replace(" ", "_")
        obj_type = ''
        if obj:
            obj_type = obj.__class__.__name__
#        sid = data['id'];
        self.publishHandler.handle(event_type, obj_type, label, data);
        # save the data.
        #_file_name = '{}_{}.json'.format(obj.__class__.__name__,
        #                                 datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        #_full_path = os.path.join('tests/json_data', _file_name)
        #with open(_full_path, 'w') as fl:
        #    json.dump(data, fl, indent=4)

    async def get_async_home(self):
        LOGGER.info("get_async_home")
        self.async_home = AsyncHome(self.loop)
        LOGGER.debug("AuthToken="+self.hmip_authtoken)
        LOGGER.debug("AccessPoint="+self.hmip_accesspoint)
        self.async_home.set_auth_token(self.hmip_authtoken)
        await self.async_home.init(self.hmip_accesspoint)
        return self.async_home
    
    def get_home(self):
        self.home = Home()
        self.home.set_auth_token(self.hmip_authtoken)
        self.home.init(self.hmip_accesspoint)

    async def update_state(self):
        LOGGER.info("update_state "+str(self.async_home))
        await self.async_home.get_current_state()
        LOGGER.info("update_start success")
        for d in self.async_home.devices:
            LOGGER.debug('{} {} {}'.format(d.id, d.label, str(d)))
        for d in self.async_home.groups:
            LOGGER.debug('{} {} {}'.format(d.id, d.label, str(d)))
    
    
    async def wait_for_ws_incoming(self):
        await self.async_home.get_current_state()
        for d in self.async_home.devices:
            d.on_update(self.on_update_handler)
        for d in self.async_home.groups:
            d.on_update(self.on_update_handler)
        reader = await self.async_home.enable_events()
        await reader
    
    def readConfiguration(self):
        self.home.get_current_state()
        LOGGER.debug("Devices:")
        for d in self.home.devices:
            LOGGER.debug('  {} {} {}'.format(d.id, d.label, str(d)))
        LOGGER.debug("Devices:")
        for g in self.home.groups:
            LOGGER.debug('  {} {} {}'.format(g.id, g.label, str(g)))
            if hasattr(g, 'profiles'):
                LOGGER.debug("Profiles for Group {}".format(g.label))
                for p in g.profiles:
                    p.get_details();
                    LOGGER.debug("  {}".format(str(p)))
#        self.jsonConf = self.async_home.download_configuration()
#        LOGGER.debug("Configuration: \n{}".format(self.jsonConf))
        
        
    def setup(self):
        self.loop = asyncio.get_event_loop()
        
        self.get_home()
        self.readConfiguration()
        
        self.async_home = None
        try:
            self.async_home = self.loop.run_until_complete(self.get_async_home())
#            self.loop.run_until_complete(self.readConfiguration())
        except HmipConnectionError:
            LOGGER.error("Problem connecting [get home]")
        if self.async_home:   
            try:
                self.loop.run_until_complete(self.update_state())
            except HmipConnectionError:
                LOGGER.error("Problem connecting [update state]")
                
                
#        loop.close()
#        self.doLoop(None)
        

    def doLoop(self, mqttClient):
        self.mqtt_client = mqttClient
        self.publishHandler = HmipPublishHandler(mqttClient)
        LOGGER.info("HomematicIp Loop Start")
        try:
            self.loop.run_until_complete(self.wait_for_ws_incoming())
        except HmipConnectionError:
            LOGGER.error("Problem connecting [incoming]")
        except KeyboardInterrupt:
            self.loop.run_until_complete(self.async_home.close_websocket_connection())
        print("HomematicIp Loop End")
