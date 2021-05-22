# -*- coding: utf-8 -*-
# @Time    : 3/31/2021 3:08 PM
# @Author  : Rex Yu
# @Mail    : jiafish@outlook.com
# @Github  : https://github.com/Rexyyj

import base64
import cherrypy
import cv2
import json
import pickle

class ImageManager():
    exposed = True

    def __init__(self, folder):
        self.folder = folder

    def GET(self, *uri, **params):
        uriLen = len(uri)
        if uriLen == 1:
            filename = uri[0] + ".jpg"
            path = self.folder + filename
            img = cv2.imread(path)
            msg = {"img":self.im2json(img)}
        return json.dumps(msg)

    def exactImageFromResponse(self,response):
        data = response.text
        imgs = json.loads(data)["img"]
        img = self.json2im(imgs)
        return img

    def im2json(self,im):
        """Convert a Numpy array to JSON string"""
        imdata = pickle.dumps(im)
        jstr = json.dumps({"image": base64.b64encode(imdata).decode('ascii')})
        return jstr

    def json2im(self,jstr):
        """Convert a JSON string back to a Numpy array"""
        load = json.loads(jstr)
        imdata = base64.b64decode(load['image'])
        im = pickle.loads(imdata)
        return im

if __name__=="__main__":
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tool.session.on': True
        }
    }
    # set this address to host ip address to enable dockers to use REST api
    cherrypy.server.socket_host='192.168.43.122'
    cherrypy.config.update({'server.socket_port': 8091})
    cherrypy.quickstart(ImageManager("./records/images"), '/',config=conf)
    cherrypy.engine.start()
    cherrypy.engine.block()
