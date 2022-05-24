#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

import cv2
import time
import argparse
import roslibpy
import json
import base64
from flask import Flask, request, session, jsonify
from flask_session import Session
from flask_socketio import SocketIO
from flask_cors import cross_origin, CORS
from models import db2
from db_utils import Database
from ros_utils import SeBot
from ros_utils import SeBot
from db_utils import Database


app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}}, automatic_options=True, supports_credentials=True)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return "<h1> HI </h1>"

@app.route('/register', methods=['POST',"GET"]) # 회원가입 화면
@cross_origin()
def register():
    if request.method == 'POST': # POST 형식으로 요청할 것임
    
        # 페이지에서 입력한 값을 받아와 변수에 저장
        userId = request.form['regi_id'] #userid
        userPwd = request.form['regi_pw'] #userpassword
        userPwd_check = request.form['regi_pw_check'] #userpassword
        userName = request.form['regi_name'] # userName
        userCode = request.form['regi_code'] # usercode
        userNumber = request.form['regi_number'] # usernumber
  
        if userPwd_check != userPwd:
            return jsonify({'ERROR' : 'NOT SAME Password and Check_Password.'}),411
          
        
        sql = 'INSERT INTO member_info("user_id", "user_pwd", "user_name", "user_code", "user_number") VALUES (%s, %s, %s, %s, %s)' # 실행할 SQL문
        
        try:
            db.execute(sql,(userId, userPwd, userName, userCode, userNumber,)) # 메소드로 전달해 명령문을 실행#
            return jsonify({'SUCCESS': 'register'}),200  # 로그인 화면으로 이동
        
        except:
            db.cursor.rollback() # 데이터베이스에 대한 모든 변경사항을 되돌림
            return jsonify({'ERROR' : 'Register Failed'}),415
         
    return jsonify({'ERROR' : 'Posting Error'}),416 # 용도 확인


@app.route('/login', methods=['POST',"GET"])
def login():
    print('login')
    if request.method == 'POST':
        userId = request.form['id']
        userPwd = request.form['pw']
        if len(userId) == 0 or len(userPwd) == 0:
            return jsonify({'ERROR' : 'Please enter your ID and Password'}),400

        else:
            sql = 'select idx, user_id, user_pwd, user_code, user_name, user_type from member_info where (user_id = %s or user_code = %s) and user_pwd = %s'
            rows = db.execute(sql, (userId, userId, userPwd,))

            if rows is None:
                return jsonify({'ERROR' : 'NOT Exist ID or Password'}),401

            else:
                for rs in rows:
                    if (userId == rs[1] and userPwd == rs[2])or(userId == rs[3] and userPwd == rs[2]): #회원 코드로도 로그인 가능
                        session['logFlag'] = True
                        session['idx'] = rs[0]
                        session['userId'] = rs[4]
                        session['userType'] = rs[5]
                        print(session) ## 출력이 되므로 session에 저장이 되어 있음
                        return jsonify({'SUCCESS': 'login', "data" : session['userType'], "ID": session['userId']}), 200

                    else:
                        return jsonify({'ERROR' : 'Login Failed'}), 400 #메소드를 호출
    else:
        return jsonify({'ERROR' : 'Posting Error'}), 402



@app.route('/info', methods=['POST',"GET"])
def info():
    if request.method == 'POST':
        login_status = request.form["login_status"]
        
        if login_status != "True" :
            return jsonify({'ERROR' : 'Not login'}),402
        else:
            userId = session["userId"]
            userType = session["userType"]
            print(userId, userType)
            
            try:
                return jsonify({'SUCCESS': 200, 'Data' : userId, "Type": userType}), 200   
            except:
                return jsonify({'ERROR' : 'Load Failed'}), 405
    else:
        return jsonify({'ERROR' : 'Posting Error'}),401

## 로그아웃 할 경우에, 다시 로그인 화면으로 돌아가게 하고, session을 clear 한다.

# Send Destination
@app.route("/call_sebot", methods=['POST'])
def call_sebot():
    print('Call SEBOT')
    if request.headers["Content-Type"] != "application/json":
        return "INVALID_ACCESS", 406
    
    data = json.loads(request.get_data()) # json error detector needed

    if (not 'idx' in data):
        return "INVALID_INPUT", 406

    idx = data['idx']

    if not type(idx) is int:
        return "INVALID_INPUT", 406

    # if not sebot.idle:
    #     return "SEBOT_BUSY", 423

    sebot.user_id = session['idx']

    start_point = db.get_map_location(idx)
    
    ros_request = roslibpy.ServiceRequest({"goal": {
        "header": {"frame_id": "map"},
        "pose": {"position": {"x": start_point[0], "y": start_point[1]},
                "orientation": {"w": 1}
                }
    }})
    
    result = sebot.goal_srv.call(ros_request)
    
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

    # if not sebot.idle:
    #     return "SEBOT_BUSY", 423
    

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


@app.route("/get_image_list", methods=['GET'])
def get_image_list():
    print(session)
    nurse_idx = session['idx']
    # nurse_idx = 33
    image_info_query = 'SELECT e.idx, e.file_name, mem.user_name FROM emergency AS e INNER JOIN member_info AS mem ON e.user_idx = mem.idx WHERE nurse_idx = %s ORDER BY e.idx DESC'
    tmp = db.execute(image_info_query, (nurse_idx,))
    res = []

    for row in tmp:
        new_row = {}
        new_row['idx'] = row[0]
        new_row['data'] = db.get_image_info(row[0])
        res.append(new_row)

    return jsonify(res)

# Socket
@app.route("/get_map", methods=['POST'])
def get_map():
    world_map = db.map.copy()

    data = json.loads(request.get_data()) # json error detector needed
    
    if (not 'location' in data):
        return "INVALID_INPUT", 406
    
    x,y = list(map(float, data['location'].split(',')))
    # print(data['location'].split(','))
    print(x, y)
    world_map = cv2.circle(world_map, (int((50 + x)*10), int((50 - y)*10)), 5, (0, 0, 255), -1)
    # world_map = cv2.imencode('_.jpg', world_map)[1].tobytes()
    world_map = cv2.imencode('_.jpg', world_map)[1]
    b64_string = base64.b64encode(world_map).decode('utf-8')

    return jsonify({'map': b64_string})


# Socket
@socketio.on('robot location')
def robot_location():
    print("Robot Location")
    map = db.map.copy()
    map = cv2.circle(map, (int((50+sebot.x)*10), int((50-sebot.y)*10)), 5, (0, 0, 255), -1)
    map = cv2.imencode('_.jpg', map)[1].tobytes()

    time.sleep(2)
    socketio.emit('state', {'map': map, 'arrival': sebot.arrival})
    
    if sebot.arrival:
        sebot.arrival = False
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--robot-ip", type=str, help="robot's ip")
    args = parser.parse_args()
    db = Database()
    sebot = SeBot(db, args.robot_ip, socketio)
    
    
    # app.debug = True
    # app.run(port=5000, debug = True)
    socketio.run(app, host="0.0.0.0", port=5000, debug=False)