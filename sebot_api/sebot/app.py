#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

import json
import cv2
import psycopg2
import time
import roslibpy
import argparse
from flask import Flask, request, session, render_template, redirect, url_for, Response, stream_with_context, jsonify
from flask_socketio import SocketIO
from flask_cors import cross_origin, CORS
# from PIL import Image
# from ros_utils import SeBot
# from db_utils import Database

app = Flask(__name__)
app.config['CORS_SUPPORTS_CREDENTIALS'] = True
CORS(app, resources={r"/*": {"origins": "*"}}, automatic_options=True)
socketio = SocketIO(app, cors_allowed_origin="* ")

@app.route("/robot_state", methods=['GET'])
def robot_state():
    # change it to socket io
    def generate():
        while 1:
            yield f'hi'
            time.sleep(5)

    return app.response_class(stream_with_context(generate()))


@socketio.on('my event')
@cross_origin()
def handle_my_custom_event(json):
    print('received my event: ' + str(json))
    # socketio.emit('my response', json, callback=messageReceived)



if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument("--robot-ip", type=str, help="robot's ip")
    # args = parser.parse_args()

    # sebot = SeBot(args.robot_ip)
    # db = Database()

    app.secret_key = '20200601'
    # app.debug = True
    # app.run(host="0.0.0.0", port=5000)
    socketio.run(app, debug=True)