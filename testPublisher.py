# -*- coding: utf-8 -*-
# @Time    : 3/31/2021 4:38 PM
# @Author  : Rex Yu
# @Mail    : jiafish@outlook.com
# @Github  : https://github.com/Rexyyj

from common.MyMQTT import *
import time
import json


class TestPublisher():

    def __init__(self):
        self.id = "test1235"
        self.topic = "/Polito/iot/SMMS/museum01/mainSwitch"
        self.broker = "test.mosquitto.org"
        self.port = 1883
        self.__msg = {"msg":"switch test"}
        self.client = MyMQTT(self.id, self.broker, self.port, None)

    def start(self):
        self.client.start()

    def stop(self):
        self.client.stop()

    def publish(self):
        msg = self.__msg
        msg["timestamp"] = str(time.time())
        self.client.myPublish(self.topic, msg)
        print("Published: " + json.dumps(msg))


if __name__ == "__main__":
    testPublisher = TestPublisher()
    testPublisher.start()
    time.sleep(1)

    while True:
        t = input("Input test rounds(nubmer) or q to quit\n")
        if t == "q":
            break
        else:
            number = int(t)
            for i in range(number):
                testPublisher.publish()
                time.sleep(3)

    testPublisher.stop()
