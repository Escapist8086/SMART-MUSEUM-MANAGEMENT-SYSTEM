# -*- coding: utf-8 -*-
"""
Created on Thu May  6 00:17:44 2021

@author: shao
"""

from RegManager import *
from MyMQTT import *
import json
import time
import requests


 
    
class lightcontrol():
    def __init__(self,clientID,topic,broker,port):
        
        #self.regManager=RegManager()
        self.clientID = clientID
        self.port = port
        self.topic= topic
        self.broker= broker
        self.client=MyMQTT(clientID,self.broker,self.port,self)
        self.zone={'zone1':0,
                   'zone2':0,
                   'zone3':0,
                   'zone4':0}
        #getdata=self.regManager.get_data()
        self.light={'light1':0,
                    'light2':0,
                    'light3':0,
                    'light4':0}
        
    
    def start(self):
        self.client.start()
        self.client.mySubscribe(self.topic)

    def stop(self):
        self.client.stop()

    def notify(self,topic,msg):
        
        payload=json.loads(msg)    
        
        laserID=payload["laserID"]
        enter=int(payload['enter'])
        leaving=int(payload['leaving'])
        
        if laserID == "laser0":
            self.zone['zone1']+=enter
            self.zone['zone1']-=leaving
        elif laserID == "laser1":
            self.zone['zone2']+=enter
            self.zone['zone2']-=leaving
            self.zone['zone1']-=enter
            self.zone['zone1']+=leaving
        elif laserID == "laser2":
            self.zone['zone3']+=enter
            self.zone['zone3']-=leaving
            self.zone['zone2']-=enter
            self.zone['zone2']+=leaving
        elif laserID == "laser3":
            self.zone['zone4']+=enter
            self.zone['zone4']-=leaving
            self.zone['zone3']-=enter
            self.zone['zone3']+=leaving
        else:
            pass

        if self.zone['zone1'] == 0:
            if self.light['light1'] == 1:
                self.light['light1'] = 0
                Message={"lightControllerId":["light1"],"timestamp":time.time(),"brightness":0}
                self.client.myPublish("/Polito/iot/SMMS/museum01/mainSwitch",json.dumps(Message))

            elif self.light['light1'] == 0:
                 pass
        else:
            if self.light['light1'] == 0:
                self.light['light1'] = 1
                Message={"lightControllerId":["light1"],"timestamp":time.time(),"brightness":100}
                self.client.myPublish("/Polito/iot/SMMS/museum01/mainSwitch",json.dumps(Message))
                
            elif self.light['light1'] == 1:
                 pass
        if self.zone['zone2'] == 0:
            if self.light['light2'] == 1:
                self.light['light2'] = 0
                Message={"lightControllerId":["light2"],"timestamp":time.time(),"brightness":0}
                self.client.myPublish("/Polito/iot/SMMS/museum01/mainSwitch",json.dumps(Message))
                
            elif self.light['light2'] == 0:
                 pass
        else:
            if self.light['light2'] == 0:
                self.light['light2'] = 1
                Message={"lightControllerId":["light2"],"timestamp":time.time(),"brightness":100}
                self.client.myPublish("/Polito/iot/SMMS/museum01/mainSwitch",json.dumps(Message))
                
            elif self.light['light2'] == 1:
                 pass
        if self.zone['zone3'] == 0:
            if self.light['light3'] == 1:
                self.light['light3'] = 0
                Message={"lightControllerId":["light3"],"timestamp":time.time(),"brightness":0}
                self.client.myPublish("/Polito/iot/SMMS/museum01/mainSwitch",json.dumps(Message))
                
            elif self.light['light3'] == 0:
                 pass  
        else:
            if self.light['light3'] == 0:
                self.light['light3'] = 1
                Message={"lightControllerId":["light3"],"timestamp":time.time(),"brightness":100}
                self.client.myPublish("/Polito/iot/SMMS/museum01/mainSwitch",json.dumps(Message))
                
            elif self.light['light3'] == 1:
                 pass
        if self.zone['zone4'] == 0:
            if self.light['light4'] == 1:
                self.light['light4'] = 0
                Message={"lightControllerId":["light4"],"timestamp":time.time(),"brightness":0}
                self.client.myPublish("/Polito/iot/SMMS/museum01/mainSwitch",json.dumps(Message))
                
            elif self.light['light4'] == 0:
                 pass
        else:
            if self.light['light4'] == 0:
                self.light['light4'] = 1
                Message={"lightControllerId":["light4"],"timestamp":time.time(),"brightness":100}
                self.client.myPublish("/Polito/iot/SMMS/museum01/mainSwitch",json.dumps(Message))
                
            elif self.light['light4'] == 1:
                 pass      
        
        self.client.myPublish("yourtopic",json.dumps(self.light))#传输topic需要跟thinkspeak  
        print(self.light)
        


if __name__=="__main__":
    #manager=RegManager('172.0.0.1:8080')
    #getdata=manager.getData('devices','type','floor=2&enterZone=zone1')
    #topic = getdata["topic"]
    port = 1883
    topic='/Polito/iot/SMMS/museum01/floor1/gate1/laser'
    broker='localhost' #其他人运行时请修改
    yourtest = lightcontrol("lightControllerId",topic,broker,port)
    yourtest.start()
    
    while (True):
        pass
