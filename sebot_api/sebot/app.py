#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

import json
import cv2
import threading
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


@app.route("/get_image", methods=['POST'])
def get_image():
    return 400


@app.route("/call_sebot", methods=['POST'])
def call_sebot():
    if request.headers["Content-Type"] != "application/json":
        return "INVALID_ACCESS", 406
    
    data = json.loads(request.get_data()) # json error detector needed

    if (not 'target' in data) or (not 'start' in data):
        return "INVALID_INPUT", 406

    start_point = data['start']
    target_point = data['target']
    end_point = start_point[:]

    if not type(start_point) is list or len(start_point) != 2:
        return "INVALID_INPUT", 406

    if not type(target_point) is list or len(target_point) != 2:
        return "INVALID_INPUT", 406

    if not sebot.idle:
        return "SEBOT_BUSY", 423

    # SEND TARGET TO ROBOT
    sebot.idle = False
    sebot.reached = -1
    sebot.user_path.append(start_point)
    sebot.user_path.append(target_point)
    sebot.user_path.append(end_point)

    return "SUCCESS", 200


if __name__=="__main__":
    sebot_thread = threading.Thread(target=sebot.run)
    flask_thread = threading.Thread(target=app.run, args=("0.0.0.0", 5000))
    sebot_thread.start()
    flask_thread.start()