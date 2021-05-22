# -*- coding: utf-8 -*-
# @Time    : 3/31/2021 4:38 PM
# @Author  : Rex Yu
# @Mail    : jiafish@outlook.com
# @Github  : https://github.com/Rexyyj

from common.MyMQTT import *
import time
import json
class TestSubscriber():

    def __init__(self):
        self.id = "test12345"
        self.topic = "/Polito/iot/SMMS/museum01/floor1/gate1/camera"
        self.broker = "test.mosquitto.org"
        self.port = 1883
        self.client = MyMQTT(self.id, self.broker, self.port, self)

    def start(self):
        self.client.start()
        self.client.mySubscribe(self.topic)


    def stop(self):
        self.client.stop()

    def notify(self, topic, msg):
        payload = json.loads(msg)
        msg_s = json.dumps(payload)
        print("Receive msg from topic: "+topic)
        print("Msg: "+msg_s)
        print("\n")

if __name__=="__main__":
    testSubscriber =TestSubscriber()
    testSubscriber.start()
    time.sleep(1)

    while True:
        t = input("Input q to quit\n")
        if t =="q":
            break


    testSubscriber.stop()
