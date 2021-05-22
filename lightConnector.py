# -*- coding: utf-8 -*-
# @Time    : 3/31/2021 4:17 PM
# @Author  : Rex Yu
# @Mail    : jiafish@outlook.com
# @Github  : https://github.com/Rexyyj

from common.MyMQTT import *
from common.RegManager import *
import json
import time


class LightConnector():

    def __init__(self, confAddr):
        try:
            self.conf = json.load(open(confAddr))
        except:
            print("Configuration file not found")
            exit()
        self.deviceId = self.conf["deviceId"]
        self.client = MyMQTT(self.deviceId, self.conf["broker"], int(self.conf["port"]), self)
        self.workingStatus = "on"
        self.brightness = 0
        self.lightTopic = self.conf["lightTopic"]
        self.switchTopic = self.conf["switchTopic"]

        regMsg = {"registerType": "device",
                  "id": self.deviceId,
                  "type": "light",
                  "topic": self.lightTopic,
                  "attribute": {"floor": self.conf["floor"],
                                "controlZone": self.conf["controlZone"],
                                "currentBrightness": self.brightness}
                  }
        self.Reg = RegManager(self.conf["homeCatAddress"])
        self.museumSetting = self.Reg.register(regMsg)
        if self.museumSetting == "":
            exit()

    def start(self):
        self.client.start()
        self.client.mySubscribe(self.switchTopic)
        self.client.mySubscribe(self.lightTopic)

    def stop(self):
        self.client.stop()
        self.Reg.delete("device", self.conf["deviceId"])

    def notify(self, topic, msg):
        data = json.loads(msg)
        if topic == self.switchTopic:
            # ToDo: update process of input msg
            print(json.dumps(data))
            self.workingStatus = "on"
        elif topic == self.lightTopic:
            brightness = int(data["brightness"])
            self.setLightStatus(brightness)

    def setLightStatus(self, status):
        self.brightness = status
        time.sleep(1)
        print("Light " + self.deviceId + " brightness:" + str(self.brightness))


if __name__ == "__main__":

    lightConnector = LightConnector('lightConfig.json')
    lightConnector.start()
    print("Light connector is running...")

    while True:
        c = input("Enter q if want to stop motor connector")
        if c == "q":
            break

    lightConnector.stop()
