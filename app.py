from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# 데이터베이스 초기화 함수
def init_db():
    conn = sqlite3.connect('reservation.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS reservations (
        id TEXT PRIMARY KEY,
        name TEXT,
        phone TEXT,
        photo_type TEXT,
        status INTEGER DEFAULT 0
    )
    ''')
    conn.commit()
    conn.close()

init_db()

# 홈 페이지
@app.route('/')
def home():
    return render_template('home.html')

# 예약 처리
@app.route('/reservation', methods=['POST'])
def reservation():
    name = request.form['name']
    phone = request.form['phone'].replace('-', '')  # 하이픈 제거
    photo_type = request.form['photo_type']
    
    # 예약번호 생성
    conn = sqlite3.connect('reservation.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM reservations WHERE photo_type=?", (photo_type,))
    count = cursor.fetchone()[0] + 1
    
    type_code = {'프로필사진': '1', '인생네컷': '2', '폴라로이드': '3'}[photo_type]
    reservation_id = f"{type_code}{count:03}"
    
    cursor.execute("INSERT INTO reservations (id, name, phone, photo_type, status) VALUES (?, ?, ?, ?, 0)",
                   (reservation_id, name, phone, photo_type))
    
    conn.commit()
    conn.close()

    return render_template('reservation.html', name=name, phone=phone, photo_type=photo_type, reservation_id=reservation_id)

# 관리자 로그인 페이지
@app.route('/admin_login')
def admin_login():
    return render_template('admin_login.html')

# 관리자 로그인 처리
@app.route('/admin_login', methods=['POST'])
def admin_login_post():
    password = request.form['password']
    
    with open('password.txt', 'r') as f:
        correct_password = f.read().strip()
    
    if password == correct_password:
        session['admin'] = True
        return redirect(url_for('admin'))
    else:
        return render_template('admin_login.html', error="틀린 비밀번호입니다.")

# 관리자 페이지
@app.route('/admin')
def admin():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    
    conn = sqlite3.connect('reservation.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reservations")
    reservations = cursor.fetchall()
    conn.close()
    
    return render_template('admin.html', reservations=reservations)

# 예약 처리 상태 업데이트
@app.route('/update_status/<reservation_id>', methods=['POST'])
def update_status(reservation_id):
    new_status = request.form['status']
    
    conn = sqlite3.connect('reservation.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE reservations SET status = ? WHERE id = ?", (new_status, reservation_id))
    conn.commit()
    conn.close()
    
    return jsonify(success=True)

# 예약 페이지로 직접 접근 방지
@app.route('/reservation')
def reservation_redirect():
    return redirect(url_for('home'))

# 관리자 페이지로 직접 접근 방지
@app.route('/admin')
def admin_redirect():
    return redirect(url_for('admin_login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
