#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

import cv2
import time
from flask import Flask, request, session, render_template, redirect, url_for, jsonify
from flask_socketio import SocketIO
from flask_cors import cross_origin, CORS
import argparse
import roslibpy
import json
from db_utils import Database
from ros_utils import SeBot
from ros_utils import SeBot
from db_utils import Database

app = Flask(__name__)
app.host = '0.0.0.0'
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


# Send Destination
@app.route("/call_sebot", methods=['POST'])
@cross_origin()
def call_sebot():
    print('call sebot')
    if request.headers["Content-Type"] != "application/json":
        return "INVALID_ACCESS", 406
    
    data = json.loads(request.get_data()) # json error detector needed

    if (not 'idx' in data):
        return "INVALID_INPUT", 406

    idx = data['idx']

    if not type(idx) is int:
        return "INVALID_INPUT", 406

    if not sebot.idle:
        return "SEBOT_BUSY", 423

    start_point = [3, 2]

    if idx == 1:
        start_point = [-9.5, 9.5]
    


    ros_request = roslibpy.ServiceRequest({"goal": {
        "header": {"frame_id": "map"},
        "pose": {"position": {"x": start_point[0], "y": start_point[1]},
                "orientation": {"w": 1}
                }
    }})
    print('before call')
    result = sebot.goal_srv.call(ros_request)
    print('after call')
    if result['response']:
        sebot.idle = False
        sebot.arrival = False
        sebot.user_path.append(start_point)
        sebot.active_step = (sebot.active_step + 1) % 3

        return "SUCCESS", 200
    
    return "FAIL", 400


# Send Destination
@app.route("/set_dest", methods=['POST'])
def set_dest():
    if request.headers["Content-Type"] != "application/json":
        return "INVALID_ACCESS", 406
    
    data = json.loads(request.get_data()) # json error detector needed

    if (not 'dst' in data):
        return "INVALID_INPUT", 406

    dst_point = data['dst']

    if not type(dst_point) is list or len(dst_point) != 2 or not type(dst_point[0]) is int or not type(dst_point[1]) is int:
        return "INVALID_INPUT", 406

    if not sebot.idle:
        return "SEBOT_BUSY", 423
    

    ros_request = roslibpy.ServiceRequest({"goal": {
        "header": {"frame_id": "map"},
        "pose": {"position": {"x": dst_point[0], "y": dst_point[1]},
                "orientation": {"w": 1}
                }
    }})

    result = sebot.goal_srv.call(ros_request)
    
    if result['response']:
        sebot.arrival = False
        # sebot.user_path.append(dst_point)
        sebot.active_step = (sebot.active_step + 1) % 3

        return "SUCCESS", 200
    
    return "FAIL", 400


# End strolling
@app.route("/end_strolling", methods=['POST'])
def end_strolling():
    pass


@app.route("/get_image_list", methods=['POST'])
def get_image_list():
    nurse_idx = session['idx']
    image_info_query = 'SELECT e.idx, e.file_name, mem.user_name FROM emergency AS e INNER JOIN member_info AS mem ON e.user_idx = mem.idx WHERE nurse_idx = %s'
    res = db.execute(image_info_query, (nurse_idx,))
    return jsonify(res)


@app.route("/get_image", methods=['POST'])
def get_image():
    file_name = request.json['file_name']
    url = db.cloud.get_image(file_name)
    res = dict()
    res['url'] = url
    res['odom'] = [10,10]
    return jsonify(res)


# Socket
@socketio.on('robot location')
def robot_location():
    map = db.map.copy()
    map = cv2.circle(map, (int((50+sebot.x)*10), int((50-sebot.y)*10)), 5, (0, 0, 255), -1)
    map = cv2.imencode('_.jpg', map)[1].tobytes()
    print('hihihihii')

    socketio.emit('state', {'map': map, 'arrival': sebot.arrival})
    
    if sebot.arrival:
        sebot.arrival = False
    time.sleep(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--robot-ip", type=str, help="robot's ip")
    args = parser.parse_args()

    db = Database()
    sebot = SeBot(db, args.robot_ip, socketio)

    app.secret_key = '20200601'
    # app.debug = True
    # app.run(host="0.0.0.0", port=5000)
    socketio.run(app)