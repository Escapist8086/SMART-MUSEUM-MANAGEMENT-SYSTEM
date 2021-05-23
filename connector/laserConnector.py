# -*- coding: utf-8 -*-
# @Time    : 3/31/2021 3:08 PM
# @Author  : Rex Yu
# @Mail    : jiafish@outlook.com
# @Github  : https://github.com/Rexyyj

from common.MyMQTT import *
from common.RegManager import *
import json
import time


class LaserConnector():

    def __init__(self, confAddr):
        try:
            self.conf = json.load(open(confAddr))
        except:
            print("Configuration file not found")
            exit()
        self.deviceId = self.conf["deviceId"]
        self.client = MyMQTT(self.deviceId, self.conf["broker"], int(self.conf["port"]), self)
        self.workingStatus = "on"

        self.laserTopic = self.conf["laserTopic"]
        self.switchTopic = self.conf["switchTopic"]
        self.__msg = {"laserID": self.deviceId, "timestamp": "", "enter": 0, "leaving": 0}
        regMsg = {"registerType": "device",
                  "id": self.deviceId,
                  "type": "laser",
                  "topic": self.laserTopic,
                  "attribute": {"floor": self.conf["floor"],
                                "enterZone": self.conf["enterZone"],
                                "leavingZone": self.conf["leavingZone"]}}
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

    def publish(self, inNum, outNum):
        msg = self.__msg
        msg["timestamp"] = str(time.time())
        msg["enter"] = inNum
        msg["leaving"] = outNum
        self.client.myPublish(self.laserTopic, msg)
        print("Published: " + json.dumps(msg))

    def notify(self, topic, msg):
        data = json.loads(msg)
        print(json.dumps(data))
        # ToDo: update process of input msg
        self.workingStatus = "on"

    def manual(self):
        while True:
            if self.workingStatus == "on":
                print("Press q to leave manual mode, or enter the number of people entering zone:" + self.conf[
                    "enterZone"])
                val1 = input()
                if val1 == "q":
                    break
                print("Enter the number of people leaving zone:" + self.conf["enterZone"])
                val2 = input()
                self.publish(val1, val2)
            else:
                time.sleep(1)

    def replay(self):
        while True:
            flag = input("Enter the location of recorded data or enter q to leave: ")
            if flag == "q":
                break
            else:
                try:
                    datas = json.load(open(flag))
                except:
                    print("Record data file not found")
                    continue
                for data in datas["data"]:
                    self.publish(int(data["enter"]), int(data["leaving"]))
                    time.sleep(10)

    # def modeReader(self):
    #     print("reader running")
    #     while True:
    #         if self.workingStatus != "m":
    #             self.modeFlag = input()


if __name__ == "__main__":

    laserConnector = LaserConnector('laserConfig.json')
    laserConnector.start()
    time.sleep(1)

    while True:
        print("Please choose the working mode:")
        print("m: manual, r: replay, q: quit")
        mode = input()
        if mode == "q":
            break;
        elif mode == "m":
            laserConnector.manual()
        elif mode == "r":
            laserConnector.replay()

    laserConnector.stop()
