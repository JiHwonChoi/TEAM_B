#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

import json
from flask import Flask

from ros_utils import SeBot

app = Flask(__name__)
sebot = SeBot()

@app.route("/")
def hello():
    return "Hello World"

@app.route("/odom", methods=['GET'])
def odom():
    if sebot.x is None or sebot.y is None or sebot.z is None:
        return "NOT_INTIALIZED", 406

    res_body = {}
    res_body['x'] = sebot.x
    res_body['y'] = sebot.y
    res_body['z'] = sebot.z

    return res_body

if __name__=="__main__":
    app.run(host='0.0.0.0', port=5000)