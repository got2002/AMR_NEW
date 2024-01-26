# app.py (using Flask)
from flask import Flask, render_template, request, redirect
from datetime import datetime, timedelta

app = Flask(__name__)

# ข้อมูลจำลองสำหรับการสาธิต
last_password_change = datetime.now()

@app.route('/')
def index():
    notification = request.args.get('notification', '')
    return render_template('index.html', notification=notification)

@app.route('/change_password', methods=['POST'])
def change_password():
    global last_password_change

    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')

    # เพิ่มตรวจสอบว่ารหัสผ่านตรงและตรงตามเกณฑ์อื่น ๆ
    if current_password == "current_password" and new_password == confirm_password:
        # ตรวจสอบว่าผ่านไป 3 เดือนนับจากการเปลี่ยนรหัสผ่านครั้งล่าสุด
        if datetime.now() - last_password_change >= timedelta(days=90):
            last_password_change = datetime.now()
            notification = 'เปลี่ยนรหัสผ่านเรียบร้อย.'
        else:
            notification = 'อนุญาตให้เปลี่ยนรหัสผ่านเฉพาะทุก 3 เดือน.'
    else:
        notification = 'รหัสผ่านไม่ตรงหรือรหัสผ่านปัจจุบันไม่ถูกต้อง.'

    return redirect(f'/?notification={notification}')

if __name__ == '__main__':
    app.run(debug=True)
