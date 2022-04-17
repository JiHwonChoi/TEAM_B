from flask import Flask, request, session, render_template, redirect, url_for
from models import db

app = Flask(__name__)

@app.route('/')
def root():
    return 'root'

@app.route('/main')
def main():
    return render_template('main.html')
@app.route('/register_form')
def register_form():
    return render_template('register/register_form.html')


@app.route('/register_proc', methods=['POST']) # 회원가입 화면
def register():
    error = None
    if request.method == 'POST': # POST 형식으로 요청할 것임
        # 페이지에서 입력한 값을 받아와 변수에 저장
        userId = request.form['regi_id'] #userid
        userPwd = request.form['regi_pw'] #userpassword
        userName = request.form['regi_name'] # userName
        userCode = request.form['regi_code'] # usercode
        userNumber = request.form['regi_number'] # usernumber
        ## 변수를 추가
        conn = db # DB와 연결
        cursor = conn.cursor() # connection으로부터 cursor 생성
        sql = 'INSERT INTO member_info("user_id", "user_pwd", "user_name", "user_code", "user_number") VALUES (%s, %s, %s, %s, %s)' # 실행할 SQL문
        cursor.execute(sql,(userId, userPwd, userName, userCode, userNumber)) # 메소드로 전달해 명령문을 실행#
        data = cursor.rowcount # 실행한 결과 데이터를 꺼냄
        
        if data != 0:
            conn.commit() # 변경사항 저장
            cursor.close()
            conn.close()
            return redirect(url_for('main'))  # 로그인 화면으로 이동
            

        else:
            conn.rollback() # 데이터베이스에 대한 모든 변경사항을 되돌림
            cursor.close()
            conn.close()
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
            sql = 'select idx, user_id, user_pwd from member_info where user_id = %s and user_pwd = %s'
            #sql = 'select * from member'
            cursor.execute(sql, (userId, userPwd))
            rows = cursor.fetchall()
            if len(rows) == 0:
                return redirect(url_for('login_form'))
            else:
                for rs in rows:
                    print(rs)
                    if userId == rs[1] and userPwd == rs[2]:
                        session['logFlag'] = True
                        session['idx'] = rs[0]
                        session['userId'] = userId
                        
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
    userId = request.form.get('userId', False)
    if len('idx') == 0:
        return 'Edit Data Not Found'
    else:
        conn = db
        cursor = conn.cursor()
        sql = 'update member_info set user_pwd = %s where idx = %s'
        cursor.execute(sql,(userPwd,idx))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('main'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main'))



if __name__ == '__main__':
    app.secret_key = '20200601'
    app.debug = True
    app.run()