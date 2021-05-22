# -*- coding: utf-8 -*-
# @Time    : 3/31/2021 3:08 PM
# @Author  : Rex Yu
# @Mail    : jiafish@outlook.com
# @Github  : https://github.com/Rexyyj

from common.MyMQTT import *
from common.RegManager import *
import json
import time
import threading


class CameraConnector():

    def __init__(self, confAddr):
        try:
            self.conf = json.load(open(confAddr))
        except:
            print("Configuration file not found")
            exit()
        self.deviceId = self.conf["deviceId"]
        self.client = MyMQTT(self.deviceId, self.conf["broker"], int(self.conf["port"]), self)
        self.workingStatus = "on"

        self.cameraTopic = self.conf["cameraTopic"]
        self.switchTopic = self.conf["switchTopic"]
        self.__msg = {"id": self.deviceId, "timestamp": "", "sequenceNum": 0, "temperature": 0}
        self.sequenceNum = 0

        regMsg = {"registerType": "device",
                  "id": self.deviceId,
                  "type": "camera",
                  "topic": self.cameraTopic,
                  "attribute": {"entranceId": self.conf["entranceId"],
                                "motorControllerId": self.conf["motorControllerId"],
                                "RESTaddr": self.conf["RESTaddr"]}
                  }
        self.Reg = RegManager(self.conf["homeCatAddress"])
        self.museumSetting = self.Reg.register(regMsg)
        if self.museumSetting == "":
            exit()

    def start(self):
        self.client.start()
        self.client.mySubscribe(self.switchTopic)

    def stop(self):
        self.client.stop()
        self.Reg.delete("device", self.conf["deviceId"])

    def publish(self, sequenceNum, temp):
        msg = self.__msg
        msg["timestamp"] = str(time.time())
        msg["sequenceNum"] = sequenceNum
        msg["temperature"] = temp
        self.client.myPublish(self.cameraTopic, msg)
        print("Published: " + json.dumps(msg))

    def notify(self, topic, msg):
        data = json.loads(msg)
        print(json.dumps(data))
        # ToDo: update process of input msg
        self.workingStatus = "on"

    def replay(self):
        while True:
            record = input("Input the record file: ")
            try:
                datas = json.load(open(record))
            except:
                print("The record file not exist!")
                continue
            for data in datas["data"]:
                self.publish(data["sequence"], data["temp"])
                time.sleep(5)
            option = input("Input r: replay, q: quit\n")
            if option == "r":
                continue
            else:
                break

    def automatic(self):
        pass


if __name__ == "__main__":

    cameraConnector = CameraConnector('cameraConfig.json')

    cameraConnector.start()
    time.sleep(1)

    while True:
        print("Please choose the working mode:")
        print("r: replay, a: automatic q: quit")
        mode = input()
        if mode == "q":
            break
        elif mode == "r":
            cameraConnector.replay()
        elif mode == "a":
            cameraConnector.automatic()

    cameraConnector.stop()
