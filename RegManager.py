# -*- coding: utf-8 -*-
# @Time    : 3/31/2021 3:08 PM
# @Author  : Rex Yu
# @Mail    : jiafish@outlook.com
# @Github  : https://github.com/Rexyyj

import requests
import json


class RegManager():
    def __init__(self,homeCat):
        self.homeCat = homeCat

    def register(self, regMsg):
        reg = requests.put(self.homeCat, json.dumps(regMsg))
        response = json.loads(reg) #deleted the .txt
        if response["status"] == "fail":
            print("Register Fail!!!")
            print("Fail type: " + response["errorType"])
        else:
            print("Register Success")
        return response["setting"]

    def getData(self, fatherType, childType,params):
        uri = self.homeCat+"/"+fatherType+"/"+childType
        response = requests.get(uri,params)
        data = json.loads(response)
        return data


    def delete(self,type,id):
        requests.delete(self.homeCat + "/"+type+"/" + id)
