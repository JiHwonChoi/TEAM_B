#!/usr/bin/env python3
# _*_ coding: utf-8 _*_


import json
import cv2
from flask import Flask, request

from ros_utils import SeBot
from db_utils import Database


app = Flask(__name__)
sebot = SeBot()
db = Database()


@app.route("/")
def hello():
    res = db.execute("SELECT * FROM robot_info")
    return json.dumps(res)

@app.route("/odom", methods=['GET'])
def odom():
    if sebot.x is None or sebot.y is None or sebot.z is None:
        return "NOT_INTIALIZED", 406

    res_body = {}
    res_body['x'] = sebot.x
    res_body['y'] = sebot.y
    res_body['z'] = sebot.z

    return res_body

@app.route("/upload_image", methods=['POST'])
def upload_image():
    if sebot.img is None:
        return "NOT_INITIALIZED", 406

    res = db.image_upload(sebot.img)
    if not res:
        return "UPLOAD_FAIL", 400

    return "UPLOAD_COMPLETE", 200

@app.route("/call_sebot", methods=['POST'])
def call_sebot():
    if request.headers["Content-Type"] != "application/json":
        return "INVALID_ACCESS", 406
    
    data = json.loads(request.get_data())

    if not 'target' in data:
        return "INVALID_INPUT", 406

    target = data['target']

    if not type(target) is list or len(target) != 2:
        return "INVALID_INPUT", 406

    # SEND TARGET TO ROBOT
    sebot.publish_goal(target)

    # UPDATE ROBOT STATUS TO DB

    return "SUCCESS", 200


if __name__=="__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)