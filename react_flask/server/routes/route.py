import os
import json
from flask_cors import cross_origin
import jsonify
from flask import Flask, jsonify, request, session, render_template, redirect, url_for
from server.routes.models import db
from flask_cors import CORS


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

@app.route('/')
def index():
    return "<h1> HI </h1>"

@app.route('/register', methods=['POST']) # 회원가입 화면
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
        #userType = request.form.get('regi_admin', False) ## userType
        ## 변수를 추가
        if userPwd_check != userPwd:
            return jsonify({'ERROR' : 'NOT SAME Password and Check_Password.'}) 
          
        conn = db # DB와 연결
        cursor = conn.cursor() # connection으로부터 cursor 생성
        sql = 'INSERT INTO member_info("user_id", "user_pwd", "user_name", "user_code", "user_number") VALUES (%s, %s, %s, %s, %s)' # 실행할 SQL문
        #cursor.execute(sql,(userId, userPwd, userName, userCode, userNumber, userType)) # 메소드로 전달해 명령문을 실행#
        cursor.execute(sql,(userId, userPwd, userName, userCode, userNumber)) # 메소드로 전달해 명령문을 실행#
        data = cursor.rowcount # 실행한 결과 데이터를 꺼냄
        
        if data != 0:
            conn.commit() # 변경사항 저장
            return jsonify({'SUCCESS': 200})  # 로그인 화면으로 이동
        
        else:
            conn.rollback() # 데이터베이스에 대한 모든 변경사항을 되돌림
            return jsonify({'ERROR' : 'Register Failed'})
         
    return jsonify({'ERROR' : 'Posting Error'}) # 용도 확인