#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

import cv2
import time
from flask import Flask, request, session, render_template, redirect, url_for, Response, stream_with_context, jsonify
from flask_socketio import SocketIO
from flask_cors import cross_origin, CORS
# from PIL import Image
# from ros_utils import SeBot
# from db_utils import Database

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}}, automatic_options=True)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/robot_state", methods=['GET'])
def robot_state():
    # change it to socket io
    def generate():
        while 1:
            yield f'hi'
            time.sleep(5)

    return app.response_class(stream_with_context(generate()))


def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(json):
    print('received my event: ' + str(json))
    socketio.emit('server response', json, callback=messageReceived)

@socketio.on('robot location')
def robot_location():
    map = cv2.imread('map.pgm')
    map = cv2.circle(map, (int(10), int(10)), 5, (0, 0, 255), -1)
    map = cv2.imencode('_.jpg', map)[1].tobytes()
    socketio.emit('state', {'map': map, 'arrival': False})

if __name__ == "__main__":
    app.secret_key = '20200601'
    # app.debug = True
    # app.run(host="0.0.0.0", port=5000)
    socketio.run(app, debug=True)