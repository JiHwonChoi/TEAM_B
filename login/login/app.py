from flask import Flask #설치한 Flask 패키지에서 Flask 모듈을 import 하여 사용
import os #디렉토리 절대 경로
import sys
from flask import Flask, render_template, request, redirect, session,url_for
#from flask_sqlalchemy import SQLAlchemy
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from models import db


app = Flask(__name__)


#@app.route('/')

#def hello():
#	return 'hello world'

## 로그인 구현
@app.route('/main', methods=['GET', 'POST']) # 메인 로그인 화면
def login():
    error = None
    if request.method == 'POST': # POST 형식으로 요청할 것임
        # 페이지에서 입력한 값을 받아와 변수에 저장
        id = request.form['id']
        pw = request.form['pw']
        if len(pw) == 0 or len(id) == 0:
            return "please enter your id or password"
 
        conn = db # DB와 연결
        cursor = conn.cursor() # connection으로부터 cursor 생성
        sql = "SELECT id FROM users WHERE userid = %s AND password = %s" # 실행할 SQL문
        value = (id, pw)
        cursor.execute("set names utf8") # 한글이 정상적으로 출력이 되지 않는 경우를 위해
        cursor.execute(sql, value) # 메소드로 전달해 명령문을 실행
 
        data = cursor.fetchall() # SQL문을 실행한 결과 데이터를 꺼냄
        cursor.close()
        conn.close()

        if data:
            session['login_user'] = id # 로그인 된 후 페이지로 데이터를 넘기기 위해 session을 사용함
            return redirect(url_for('home')) # home 페이지로 넘어감 (url_for 메소드를 사용해 home이라는 페이지로 넘어간다)
        else:
            error = 'invalid input data detected !' # 에러가 발생한 경우
    return render_template('main.html', error = error)   	


## 회원가입
@app.route('/register', methods=['GET', 'POST']) # 회원가입 화면
def register():
    error = None
    if request.method == 'POST': # POST 형식으로 요청할 것임
        # 페이지에서 입력한 값을 받아와 변수에 저장
        id = request.form['regi_id']
        nickname = request.form['regi_nick']
        pw = request.form['regi_pw']
        code = request.form['regi_code']
        name = request.form['regi_name']
        ## 변수를 추가
        conn = db # DB와 연결
        cursor = conn.cursor() # connection으로부터 cursor 생성
        sql = "INSERT INTO users VALUES ('%s', '%s', '%s', '%s', '%s')" % (name, nickname, id, pw, code) # 실행할 SQL문
        cursor.execute(sql) # 메소드로 전달해 명령문을 실행
		
        data = cursor.fetchall() # 실행한 결과 데이터를 꺼냄
        
 
        if not data:
            conn.commit() # 변경사항 저장
            cursor.close()
            conn.close()
            return redirect(url_for('main.html'))  # 로그인 화면으로 이동
            

        else:
            conn.rollback() # 데이터베이스에 대한 모든 변경사항을 되돌림
            cursor.close()
            conn.close()
            return "Register Failed"
         
    return render_template('register.html', error=error) # 용도 확인


@app.route('/', methods=['GET', 'POST']) # 메인 로그인 화면
def logout():	
    session.pop('userid',None)
    return redirect('/')    		



    
if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run()