from flask import Flask, request, session, render_template, redirect, url_for
from models import db

app = Flask(__name__)

@app.route('/')
def root():
    return 'root'

@app.route('/main')
def main():
    return render_template('main.html')

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
            #sql = 'select idx, userId, userPwd from member where userId = %s and userPwd = %s'
            sql = 'select * from member'
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
    #sql = 'select userCode from member where idx = %s'
    sql = 'select * from member'
    cursor.execute(sql, (edit_idx,))
    row = cursor.fetchone()
    edit_code = row[4]
    #cursor.close()
    #conn.close()
    return render_template('users/user_info.html', edit_idx=edit_idx, edit_code=edit_code)

@app.route('/user_info_edit_proc', methods=['POST'])
def user_info_edit_proc():
    idx = request.form['idx']
    userPwd = request.form.get('userPwd', False)
    userId = request.form.get('userId',False)
    if len('idx') == 0:
        return 'Edit Data Not Found'
    else:
        conn = db
        cursor = conn.cursor()
        sql = 'update member set userPwd = %s, userId = %s where idx = %s'
        cursor.execute(sql,(userPwd, userId, idx))
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
