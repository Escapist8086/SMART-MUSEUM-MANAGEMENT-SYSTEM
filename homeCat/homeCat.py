# -*- coding: utf-8 -*-
# @Time    : 3/31/2021 3:08 PM
# @Author  : Rex Yu
# @Mail    : jiafish@outlook.com
# @Github  : https://github.com/Rexyyj

import cherrypy
import json


class HomeCat():
    exposed = True

    def __init__(self, configure):
        self.setting = json.load(open(configure))
        self.devices = []
        self.services = []
        self.registerStatus = {"status": "success", "errorType": "None", "setting": ""}
        self.getResult = {"status": "Success", "failType": "None", "data": []}

    def set_getResult(self, status, failType, data):
        self.getResult["status"] = status
        self.getResult["failType"] = failType
        self.getResult["data"] = data

    def set_registerStatus(self, status, errorType, setting):
        self.registerStatus["status"] = status
        self.registerStatus["errorType"] = errorType
        self.registerStatus["setting"] = setting

    def PUT(self):
        body = cherrypy.request.body.read()
        data = json.loads(body)
        errorCode = self.checkRegister(data)
        if errorCode is not None:
            self.set_registerStatus("fail", errorCode, "")
            return json.dumps(self.registerStatus)

        if data['registerType'] == "device":
            self.devices.append(data)
        else:
            self.services.append(data)
        self.set_registerStatus("success", "None", self.setting)
        json.dumps(self.registerStatus)
        return json.dumps(self.registerStatus)

    def GET(self, *uri, **params):
        uriLen = len(uri)
        if uriLen != 0:
            if uri[0] == "setting":
                return json.dumps(self.setting)
            elif uri[0] == "devices":
                # check the registered device list is empty or not
                if len(self.devices) == 0:
                    self.set_getResult("fail", "No such device registered", [])
                    return str(self.getResult)
                # select the specific type of devices
                searchDevice = []
                if uriLen == 1:
                    searchDevice = self.devices.copy()
                elif uriLen == 2:
                    for div in self.devices:
                        if div["type"] == uri[1]:
                            searchDevice.append(div)
                    if len(searchDevice) == 0:
                        self.set_getResult("fail", "No such device registered", [])
                        return str(self.getResult)
                else:
                    self.set_getResult("fail", "uri invalid", [])
                    return str(self.getResult)
                # filter out the devices not in target if param exist
                if params != {}:
                    keys = params.keys()
                    existKeys = searchDevice[0]["attribute"].keys()
                    if len(list(list(set(keys) - set(existKeys)))) != 0:
                        self.set_getResult("fail", "param not exist", [])
                        return str(self.getResult)
                    data = searchDevice.copy()
                    for key in keys:
                        for div in searchDevice:
                            if div["attribute"][key] != params[key]:
                                try:
                                    data.remove(div)
                                except:
                                    pass
                    self.set_getResult("success", "None", data)
                    return json.dumps(self.getResult)
                else:
                    self.set_getResult("success", "None", searchDevice)
                    return json.dumps(self.getResult)
            elif uri[0] == "service":
                # ToDo: add GET service operation
                pass

    def DELETE(self, *uri):
        if len(uri)==2:
            if uri[0] == "device":
                for div in self.devices:
                    if div["id"] == uri[1]:
                        self.devices.remove(div)
                        break
            elif uri[0] == "service":
                # ToDo: add DELETE operation
                pass
            else:
                pass

    def checkRegister(self, data):
        if data["registerType"] == "device":
            # check device id
            for div in self.devices:
                if div['id'] == data['id']:
                    return "Id already exist"
            # check device attributes
            try:
                if data["type"] == "laser" or data["type"] == "motorController":
                    self.setting["floors"].index(data["attribute"]["floor"])
                    self.setting["zones"].index(data["attribute"]["enterZone"])
                    self.setting["zones"].index(data["attribute"]["leavingZone"])
                elif data["type"] == "camera":
                    self.setting["entrances"].index(data["attribute"]["entranceId"])
                elif data["type"] == "lightController":
                    self.setting["floors"].index(data["attribute"]["floor"])
                    self.setting["zones"].index(data["attribute"]["controlZone"])
                else:
                    pass
            except:
                return "Device attribute not valid"
        elif data["registerType"] == "service":
            # check service id
            for ser in self.services:
                if ser['id'] == data['id']:
                    return "Id already exist"
            # check device attributes
            try:
                # ToDo: add checking according service attribute
                pass
            except:
                return "Device attribute not valid"


if __name__ == "__main__":
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tool.session.on': True
        }
    }
# set this address to host ip address to enable dockers to use REST api
cherrypy.server.socket_host='localhost'
cherrypy.config.update({'server.socket_port': 8090})
cherrypy.quickstart(HomeCat("./configuration.json"), '/', conf)
cherrypy.engine.start()
cherrypy.engine.block()
