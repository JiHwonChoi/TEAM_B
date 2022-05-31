from flask_cors import cross_origin
from flask import Flask, jsonify, redirect, request, session, url_for

from numpy import require
from server.routes.models import db
from flask_cors import CORS, cross_origin

session = {}
app = Flask(__name__)
app.secret_key = "super secret key"
CORS(app,supports_credentials=True)


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
          
        conn = db # DB와 연결
        cursor = conn.cursor() # connection으로부터 cursor 생성
        sql = 'INSERT INTO member_info("user_id", "user_pwd", "user_name", "user_code", "user_number") VALUES (%s, %s, %s, %s, %s)' # 실행할 SQL문
        
        try:
            cursor.execute(sql,(userId, userPwd, userName, userCode, userNumber)) # 메소드로 전달해 명령문을 실행#
            #conn.commit() # 변경사항 저장
            return jsonify({'SUCCESS': 'register'}),200  # 로그인 화면으로 이동
        
        except:
            conn.rollback() # 데이터베이스에 대한 모든 변경사항을 되돌림
            return jsonify({'ERROR' : 'Register Failed'}),415
         
    return jsonify({'ERROR' : 'Posting Error'}),416 # 용도 확인



@app.route('/login', methods=['POST',"GET"])
def login():

    if request.method == 'POST':
        userId = request.form['id']
        userPwd = request.form['pw']
        if len(userId) == 0 or len(userPwd) == 0:
            return jsonify({'ERROR' : 'Please enter your ID and Password'}),400
        else:
            conn = db
            cursor = conn.cursor()
            sql = 'select idx, user_id, user_pwd, user_code, user_name, user_type from member_info where (user_id = %s or user_code = %s) and user_pwd = %s'
            #sql = 'select * from member'
            cursor.execute(sql, (userId, userId, userPwd))
            rows = cursor.fetchall()
            if len(rows) == 0:
                return jsonify({'ERROR' : 'NOT Exist ID or Password'}),401
            else:
                for rs in rows:
                    if (userId == rs[1] and userPwd == rs[2])or(userId == rs[3] and userPwd == rs[2]): #회원 코드로도 로그인 가능
                        session['logFlag'] = True
                        session['idx'] = rs[0]
                        session['userId'] = rs[4]
                        session['userType'] = rs[5]
                        print(session) ## 출력이 되므로 session에 저장이 되어 있음
                        return jsonify({'SUCCESS': 'login', "data" : session['userType'], "ID": session['userId']}),200
                    else:
                        return jsonify({'ERROR' : 'Login Failed'}),400 #메소드를 호출
    else:
        return jsonify({'ERROR' : 'Posting Error'}),402



@app.route('/info', methods=['POST',"GET"])
def info():

    if request.method == 'POST':
        login_status = request.form["login_status"]
        
        if login_status != "True" :
            return jsonify({'ERROR' : 'Not login'}),402
        else:
            userId = session["userId"]
            userType = session["userType"]
            print(userId)
            print(userType)
            try:
                return jsonify({'SUCCESS': 200, 'Data' : userId, "Type": userType}), 200   
            except:
                return jsonify({'ERROR' : 'Load Failed'}), 405
    else:
        return jsonify({'ERROR' : 'Posting Error'}),401

## 로그아웃 할 경우에, 다시 로그인 화면으로 돌아가게 하고, session을 clear 한다.