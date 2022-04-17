#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
from flask import Flask, request, session, render_template, redirect, url_for
import json
import cv2
import threading
from models import db
from ros_utils import SeBot
from db_utils import Database

app = Flask(__name__)

#@app.route('/')
#def root():
#    return 'root'

@app.route("/")
def hello():
    res = db.execute("SELECT * FROM robot_info")
    return json.dumps(res)

@app.route('/main')
def main():
    return render_template('main.html')
@app.route('/register_form')
def register_form():
    return render_template('register/register_form.html')


@app.route('/register_proc', methods=['POST']) # 회원가입 화면
def register():
    #error = None
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
            return '비밀번호가 일치하지 않습니다.'   
        conn = db # DB와 연결
        cursor = conn.cursor() # connection으로부터 cursor 생성
        sql = 'INSERT INTO member_info("user_id", "user_pwd", "user_name", "user_code", "user_number", "user_type") VALUES (%s, %s, %s, %s, %s, %s)' # 실행할 SQL문
        cursor.execute(sql,(userId, userPwd, userName, userCode, userNumber, userType)) # 메소드로 전달해 명령문을 실행#
        data = cursor.rowcount # 실행한 결과 데이터를 꺼냄
        
        if data != 0:
            conn.commit() # 변경사항 저장
            #cursor.close()
            #conn.close()
            return redirect(url_for('main'))  # 로그인 화면으로 이동
            

        else:
            conn.rollback() # 데이터베이스에 대한 모든 변경사항을 되돌림
            #cursor.close()
            #conn.close()
            return "Register Failed"
         
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
            conn = db
            cursor = conn.cursor()
            sql = 'select idx, user_id, user_pwd, user_code, user_name from member_info where (user_id = %s or user_code = %s) and user_pwd = %s'
            #sql = 'select * from member'
            cursor.execute(sql, (userId, userId, userPwd))
            rows = cursor.fetchall()
            if len(rows) == 0:
                return redirect(url_for('login_form'))
            else:
                for rs in rows:
                    print(rs)
                    if (userId == rs[1] and userPwd == rs[2])or(userId == rs[3] and userPwd == rs[2]): #회원 코드로도 로그인 가능
                        session['logFlag'] = True
                        session['idx'] = rs[0]
                        session['userId'] = rs[4]
                        
                        return redirect(url_for('main'))
                    else:
                        print("here")
                        return redirect(url_for('login_form')) #메소드를 호출
    else:
        return '잘못된 접근입니다.'

@app.route('/user_info_edit/<int:edit_idx>', methods=['GET'])
def getUser(edit_idx):
    if session.get('logFlag') != True:
        return redirect('login_form')
    conn = db
    cursor = conn.cursor()
    sql = 'select user_code from member_info where idx = %s'
    #sql = 'select * from member'
    cursor.execute(sql, (edit_idx,))
    row = cursor.fetchone()
    edit_code = row[0]
    #cursor.close()
    #conn.close()
    return render_template('users/user_info.html', edit_idx=edit_idx, edit_code=edit_code)

@app.route('/user_info_edit_proc', methods=['POST'])
def user_info_edit_proc():
    idx = request.form['idx']
    userPwd = request.form.get('userPwd', False)
    #userId = request.form.get('userId', False)
    if len('idx') == 0:
        return 'Edit Data Not Found'
    else:
        conn = db
        cursor = conn.cursor()
        sql = 'update member_info set user_pwd = %s where idx = %s'
        cursor.execute(sql,(userPwd,idx))
        conn.commit()
        #cursor.close()
        #conn.close()
        return redirect(url_for('main'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main'))
## 여기까지 로그인 등등






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

if __name__ == '__main__':
    app.secret_key = '20200601'
    app.debug = True
    app.run()
    flask_thread = threading.Thread(target=app.run, args=("0.0.0.0", 5000))
    flask_thread.start()

    sebot = SeBot()
    db = Database()
    
    sebot_thread = threading.Thread(target=sebot.run)
    sebot_thread.start()
    