# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 16:45:30 2021

@author: Administrator
"""

from RegManager import *
from MyMQTT import *
import json
import time
import requests


 
    
class Customermanager():
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
      
        
    
    def start(self):
        self.client.start()
        self.client.mySubscribe(self.topic)

    def stop(self):
        self.client.stop()

    def notify(self,topic,msg):
        
        payload=json.loads(msg)    
        
        laserID=payload["laserID"]
        enter=int(payload['enter'])  # add int due to joson only transmit string,can not do +- calculation
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
            
        print("Received: "+json.dumps(payload ,indent=4))
        print("Processed: "+json.dumps(self.zone ,indent=4))


        
        self.client.myPublish("yourtopic",json.dumps(self.zone))#传输topic需要跟thinkspeak  
        
        


if __name__=="__main__":
    #manager=RegManager('http://localhost:8090/')
    #getdata=manager.getData('devices','type','floor=2&enterZone=zone1')
    #topic = getdata["topic"]
    port = 1883
    topic='/Polito/iot/SMMS/museum01/floor1/gate1/laser'
    broker='localhost' #其他人运行时请修改broker
    yourtest = Customermanager("CustormerNumber",topic, broker, port)
    yourtest.start()
    
    while (True):
        pass

 
