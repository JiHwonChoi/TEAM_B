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
from yaml import parse
from ros_utils import SeBot
from db_utils import Database

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')

@app.route('/main')
def main():
    return render_template('main.html')


@app.route('/register_form')
def register_form():
    return render_template('register/register_form.html')


@app.route('/register_proc', methods=['POST']) # 회원가입 화면
def register():
    if request.method == 'POST': # POST 형식으로 요청할 것임
        # 페이지에서 입력한 값을 받아와 변수에 저장
        userId = request.form['regi_id'] #userid
        userPwd = request.form['regi_pw'] #userpassword
        userPwd_check = request.form['regi_pw_check'] #userpassword
        userName = request.form['regi_name'] # userName
        userCode = request.form['regi_code'] # usercode
        userNumber = request.form['regi_number'] # usernumber
        userType = request.form.get('regi_admin', False) ## userType

        ## 변수를 추가
        if userPwd_check != userPwd:
            return '비밀번호가 일치하지 않습니다.', 400
        
        sql = 'INSERT INTO member_info("user_id", "user_pwd", "user_name", "user_code", "user_number", "user_type") VALUES (%s, %s, %s, %s, %s, %s)' # 실행할 SQL문
        
        try:
            db.execute(sql, (userId, userPwd, userName, userCode, userNumber, userType,))
            
        except psycopg2.IntegrityError:
            db.db.rollback()
            return f"Register Failed: IntegrityError", 400
        
    return redirect(url_for('main')) # 용도 확인


@app.route('/login_form')
def login_form():
    return render_template('login/login_form.html')


@app.route('/login_proc', methods=['POST'])
def login_proc():
    if request.method == 'POST':
        userId = request.form['id']
        userPwd = request.form['pwd']
        if len(userId) == 0 or len(userPwd) == 0:
            return 'userId, userPwd not found!!'
            
        else:
            sql = 'SELECT idx, user_id, user_pwd, user_code, user_name FROM member_info WHERE (user_id = %s or user_code = %s) and user_pwd = %s'
            rows = db.execute(sql, (userId, userId, userPwd,))

            if len(rows) == 0:
                return redirect(url_for('login_form'))

            else:
                for rs in rows:
                    if (userId == rs[1] and userPwd == rs[2])or(userId == rs[3] and userPwd == rs[2]): #회원 코드로도 로그인 가능
                        session['logFlag'] = True
                        session['idx'] = rs[0]
                        session['userId'] = rs[4]
                        
                        return redirect(url_for('main'))

                    else:
                        return redirect(url_for('login_form')) #메소드를 호출

    else:
        return '잘못된 접근입니다.', 400


@app.route('/user_info_edit/<int:edit_idx>', methods=['GET'])
def getUser(edit_idx):
    if session.get('logFlag') != True:
        return redirect('login_form')

    sql = 'SELECT user_code FROM member_info WHERE idx = %s'
    row = db.execute(sql, (edit_idx,))
    edit_code = row[0][0]
    return render_template('users/user_info.html', edit_idx=edit_idx, edit_code=edit_code)

@app.route('/user_info_edit_proc', methods=['POST'])
def user_info_edit_proc():
    idx = request.form['idx']
    userPwd = request.form.get('userPwd', False)
    
    if len('idx') == 0:
        return 'Edit Data Not Found', 400

    else:
        sql = 'UPDATE member_info SET user_pwd = %s WHERE idx = %s'
        db.execute(sql, (userPwd, idx))
        return redirect(url_for('main'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main'))


@socketio.on('robot location')
def robot_location():
    map = db.map.copy()
    map = cv2.circle(map, (int((50+sebot.x)*10), int((50-sebot.y)*10)), 5, (0, 0, 255), -1)
    map = cv2.imencode('_.jpg', map)[1].tobytes()
    socketio.emit('state', {'map': map, 'arrival': False})


@app.route("/odom", methods=['GET'])
def odom():
    if not sebot.client.is_connected:
        return "ROBOT_IS_OFF", 406

    if sebot.x is None or sebot.y is None or sebot.z is None:
        return "NOT_INTIALIZED", 406

    # change it to socket io
    def generate():
        while 1:
            yield f'x: {sebot.x}, y: {sebot.y}, reached:{sebot.reached}, step:{sebot.active_step}'
            time.sleep(5)

    return app.response_class(stream_with_context(generate()))


@app.route("/get_image", methods=['POST'])
def get_image():
    #For manager
    return 400


@app.route("/call_sebot", methods=['POST'])
def call_sebot():
    if request.headers["Content-Type"] != "application/json":
        return "INVALID_ACCESS", 406
    
    data = json.loads(request.get_data()) # json error detector needed

    if (not 'start' in data):
        return "INVALID_INPUT", 406

    start_point = data['start']

    if not type(start_point) is list or len(start_point) != 2 or not type(start_point[0]) is int or not type(start_point[1]) is int:
        return "INVALID_INPUT", 406

    if not sebot.idle:
        return "SEBOT_BUSY", 423
    
    # SEND TARGET TO ROBOT
    sebot.idle = False
    sebot.reached = 0
    sebot.user_path.append(start_point)

    goal_publisher = roslibpy.Topic(sebot.client, "move_base_simple/goal", "geometry_msgs/PoseStamped")
    goal_publisher.publish(roslibpy.Message({"header": {"frame_id": "map"},
                                                    "pose": {"position": {"x": start_point[0], "y": start_point[1]},
                                                            "orientation": {"z": 1}
                                                            }
                                                }))
    goal_publisher.unadvertise()
    sebot.active_step += 1

    return "SUCCESS", 200


@app.route("/set_dest", methods=['POST'])
def set_dest():
    if request.headers["Content-Type"] != "application/json":
        return "INVALID_ACCESS", 406
    
    data = json.loads(request.get_data()) # json error detector needed

    if (not 'dest' in data):
        return "INVALID_INPUT", 406

    dst_point = data['dest']

    if not type(dst_point) is list or len(dst_point) != 2 or not dst_point[0].isdigt() or not dst_point[1].isdigit():
        return "INVALID_INPUT", 406
    
    # SEND TARGET TO ROBOT
    sebot.reached = 0

    goal_publisher = roslibpy.Topic(sebot.client, "move_base_simple/goal", "geometry_msgs/PoseStamped")
    goal_publisher.publish(roslibpy.Message({"header": {"frame_id": "map"},
                                                    "pose": {"position": {"x": dst_point[0], "y": dst_point[1]},
                                                            "orientation": {"z": 1}
                                                            }
                                                }))
    goal_publisher.unadvertise()
    sebot.active_step = (sebot.active_step + 1) % 3

    return "SUCCESS", 200


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--robot-ip", type=str, help="robot's ip")
    args = parser.parse_args()

    db = Database()
    sebot = SeBot(db, args.robot_ip)

    app.secret_key = '20200601'
    # app.debug = True
    # app.run(host="0.0.0.0", port=5000)
    socketio.run(app, debug=True)