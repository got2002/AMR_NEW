# app.py
from flask_mail import Mail, Message
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from werkzeug.security import generate_password_hash, check_password_hash
from models import User  # Import the User model from models.py
from forms import LoginForm, RegisterForm, EditUserForm  # Import the forms

import cx_Oracle
import pandas as pd
import random
import string

app = Flask(__name__)
# ตั้งค่า database URI และ SECRET_KEY ให้ Flask app
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# app.config['SECRET_KEY'] = 'your_secret_key'  # Change to your own secret key
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
# mail = Mail(app)

# ส่วนที่ขาดหายไปใน fetch_data
hostname = 'localhost'
port = '1521'
service_name = 'orcl'
username = 'root'
password = 'root'

# MAIL_SERVER = 'Nattapong@pims.co.th'
# MAIL_PORT = 587
# MAIL_USE_TLS = True
# MAIL_USERNAME = 'Nattapong@pims.co.th'
# MAIL_PASSWORD = 'Csgop@90'

app = Flask(__name__)
# app.config['SECRET_KEY'] = '1112'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'oracle://username:password@host:port/service_name'


# กำหนดหน้าแรกที่แสดง
@app.route('/')
def home():
    return render_template('search_result.html')


def fetch_data(query, params=None):
    try:
        dsn = cx_Oracle.makedsn(hostname, port, service_name)
        with cx_Oracle.connect(username, password, dsn) as connection:
            with connection.cursor() as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                results = cursor.fetchall()
        return results
    except cx_Oracle.Error as e:
        error, = e.args
        print("Oracle Error:", error)
        return []

# ส่วนที่ขาดหายไปใน get_tags


@app.route('/get_tags', methods=['GET'])
def get_tags():
    selected_region = request.args.get('selected_region')

    tag_query = """
    SELECT DISTINCT TAG_ID
    FROM AMR_FIELD_ID
    JOIN AMR_PL_GROUP ON AMR_FIELD_ID.FIELD_ID = AMR_PL_GROUP.FIELD_ID 
    WHERE AMR_PL_GROUP.PL_REGION_ID = :region_id
    """

    tag_results = fetch_data(tag_query, params={'region_id': selected_region})
    tag_options = [str(tag[0]) for tag in tag_results]

    return jsonify({'tag_options': tag_options})

# ปรับแต่งส่วนที่ขาดหายไปใน index


@app.route('/')
def search_result():
    # SQL query to fetch unique PL_REGION_ID values
    region_query = """
    SELECT * FROM AMR_REGION 
    """
    tag_query = """
    SELECT DISTINCT TAG_ID
    FROM AMR_FIELD_ID
    JOIN AMR_PL_GROUP ON AMR_FIELD_ID.FIELD_ID = AMR_PL_GROUP.FIELD_ID 
    WHERE AMR_PL_GROUP.PL_REGION_ID = :region_id
    """
    # Fetch unique region values
    region_results = fetch_data(region_query)
    region_options = [str(region[0]) for region in region_results]

    # SQL query for main data
    query = """
    SELECT
        AMR_PL_GROUP.PL_REGION_ID,
        AMR_FIELD_ID.TAG_ID,
        amr_field_id.meter_id,
        AMR_BILLING_DATA.DATA_DATE as DATA_DATE,
        AMR_BILLING_DATA.CORRECTED_VOL as CORRECTED,
        AMR_BILLING_DATA.UNCORRECTED_VOL as UNCORRECTED,
        AMR_BILLING_DATA.AVR_PF as Pressure,
        AMR_BILLING_DATA.AVR_TF as Temperature
    FROM
        AMR_FIELD_ID, AMR_PL_group, AMR_BILLING_DATA
    WHERE
        AMR_PL_GROUP.FIELD_ID = AMR_FIELD_ID.FIELD_ID 
        AND AMR_BILLING_DATA.METER_ID = AMR_FIELD_ID.METER_ID
        AND AMR_BILLING_DATA.METER_STREAM_NO like '1'
        {date_condition}
        {tag_condition}
        {region_condition}
    """

    # Get selected values from the dropdowns
    date_condition = "AND AMR_BILLING_DATA.DATA_DATE IS NOT NULL"
    tag_condition = "AND AMR_FIELD_ID.TAG_ID IS NOT NULL"
    region_condition = "AND amr_pl_group.pl_region_id IS NOT NULL"

    selected_date = request.args.get('date_dropdown')
    selected_tag = request.args.get('tag_dropdown')
    selected_region = request.args.get('region_dropdown')

    # Fetch unique region values
    region_results = fetch_data(region_query)
    region_options = [str(region[0]) for region in region_results]

    # Fetch tag options based on the selected region
    tag_results = fetch_data(tag_query, params={'region_id': selected_region})
    tag_options = [str(tag[0]) for tag in tag_results]

    if selected_date:
        # ปรับ format ใน date_condition เพื่อให้ตรงกับรูปแบบที่ datepicker กำหนด
        date_condition = f"AND TO_CHAR(AMR_BILLING_DATA.DATA_DATE, 'MM/YYYY') = '{selected_date}'"

    if selected_tag:
        tag_condition = f"AND AMR_FIELD_ID.TAG_ID = '{selected_tag}'"
    if selected_region:
        region_condition = f"AND amr_pl_group.pl_region_id = '{selected_region}'"

    # Modify the query with the selected conditions
    query = query.format(date_condition=date_condition,
                         tag_condition=tag_condition, region_condition=region_condition)

    # ใช้ fetch_data function ในการดึงข้อมูล
    results = fetch_data(query)

    # ใช้ pandas ในการสร้าง DataFrame
    df = pd.DataFrame(results, columns=[
        'PL_REGION_ID', 'TAG_ID', 'METER_ID', 'DATA_DATE', 'CORRECTED', 'UNCORRECTED', 'Pressure', 'Temperature'
    ])

    # # ลบคอลัมน์ที่ไม่ต้องการ
    # df = df.drop(['PL_REGION_ID', 'TAG_ID', 'METER_ID'], axis=1)
    # df = df.applymap(lambda x: x.replace('\n', '')
    #                  if isinstance(x, str) else x)

    # ส่ง DataFrame ไปยัง HTML template
    return render_template('search_result.html', tables=[df.to_html(classes='data')],
                           titles=df.columns.values,
                           selected_date=selected_date,
                           selected_tag=selected_tag,
                           selected_region=selected_region,
                           region_options=region_options,
                           tag_options=tag_options)


@app.route('/your_api_endpoint')
def your_api_endpoint():
    # ตัวอย่างข้อมูลที่จะส่งกลับในรูปแบบ JSON
    tag_options = ['tag1', 'tag2', 'tag3']

    # ส่ง JSON response กลับไปยัง client
    return jsonify({'tag_options': tag_options})


def generate_token():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))


def send_reset_email(user):
    token = user.reset_token
    reset_url = url_for('reset_password', token=token, _external=True)

    msg = Message('Password Reset Request',
                  sender=app.config['MAIL_USERNAME'], recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{reset_url}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()

        if user:
            token = generate_token()
            user.reset_token = token
            db.session.commit()

            send_reset_email(user)

            flash(
                'An email has been sent with instructions to reset your password.', 'info')
            return redirect(url_for('login'))
        else:
            flash('Email not found. Please try again.', 'danger')

    return render_template('forgot_password.html')


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.query.filter_by(reset_token=token).first()

    if not user:
        flash('Invalid or expired reset token. Please try again.', 'danger')
        return redirect(url_for('forgot_password'))

    if request.method == 'POST':
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password == confirm_password:
            user.password = password
            user.reset_token = None
            db.session.commit()

            flash(
                'Password reset successful! You can now log in with your new password.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Password and Confirm Password do not match.', 'danger')

    return render_template('reset_password.html', token=token)


# สร้างโมเดล User


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)

# เพิ่มผู้ใช้ใหม่


@app.route('/add-user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        new_username = request.form['new_username']
        new_email = request.form['new_email']
        new_role = request.form['new_role']
        new_password = request.form['new_password']

        # ตรวจสอบว่ามีชื่อผู้ใช้หรืออีเมลนี้ในฐานข้อมูลแล้วหรือไม่
        existing_user = User.query.filter(
            (User.username == new_username) | (User.email == new_email)).first()

        if existing_user:
            flash(
                'Username or Email already exists. Please choose different ones.', 'danger')
        else:
            # สร้างผู้ใช้ใหม่
            new_user = User(username=new_username, email=new_email,
                            role=new_role, password=new_password)
            db.session.add(new_user)
            db.session.commit()
            flash('User added successfully!', 'success')
            # เปลี่ยนเป็น URL ที่ต้องการให้กลับหลังจากเพิ่มผู้ใช้
            return redirect('/add-user')

    # ชื่อเทมเพลตให้ตรงกับชื่อไฟล์ HTML ที่เก็บ form
    return render_template('add_user.html')

# ลบผู้ใช้


@app.route('/delete-user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)

    if user:
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully!', 'success')
        # ส่ง JSON response กลับไปยัง client
        return jsonify({'message': 'User deleted successfully'})

    # ส่ง JSON response กลับไปยัง client ว่าไม่พบผู้ใช้
    return jsonify({'message': 'User not found'}), 404


# แก้ไขข้อมูลผู้ใช้
@app.route('/edit-user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get(user_id)

    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        user.role = request.form['is_admin']

        new_password = request.form['password']
        if new_password:
            user.password = new_password

        db.session.commit()
        flash('User updated successfully!', 'success')
        # เปลี่ยนเป็น URL ที่ต้องการให้กลับหลังจากแก้ไขผู้ใช้
        return redirect('/edit-user/{}'.format(user_id))

    # ชื่อเทมเพลตให้ตรงกับชื่อไฟล์ HTML ที่เก็บ form
    return render_template('edit_user.html', user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # ค้นหาผู้ใช้จากฐานข้อมูล
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id  # เก็บ user ID ใน session
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('login.html')

# Register route


# การลงทะเบียนผู้ใช้
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # ตรวจสอบว่ามีชื่อผู้ใช้หรืออีเมลนี้ในฐานข้อมูลแล้วหรือไม่
        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
        elif password != confirm_password:
            flash('Passwords do not match. Please try again.', 'danger')
        else:
            # ทำการเข้ารหัสรหัสผ่านและบันทึกข้อมูลผู้ใช้ในฐานข้อมูล
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, email=email,
                            password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')

# Update user route


@app.route('/update-user', methods=['POST'])
def update_user():
    form = EditUserForm(request.form)

    if form.validate():
        username = form.username.data
        email = form.email.data
        is_admin = form.is_admin.data
        new_password = form.password.data

        user_id = session.get('user_id')  # Get user ID from session
        if user_id:
            user = get_user_by_id(user_id)
            if user:
                new_data = {
                    'username': username,
                    'email': email,
                    'is_admin': is_admin
                    # Add more fields if needed
                }
                update_user(user, new_data)
                flash('User updated successfully!', 'success')
                return redirect(url_for('some_page'))

    flash('Invalid data. Please try again.', 'danger')
    return redirect(url_for('some_page'))


# ส่วนที่ขาดหายไปใน reset_password
@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.query.filter_by(reset_token=token).first()

    if not user:
        flash('Invalid or expired reset token. Please try again.', 'danger')
        return redirect(url_for('forgot_password'))

    if request.method == 'POST':
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password == confirm_password:
            # บันทึกรหัสผ่านใหม่ลงในฐานข้อมูล
            user.password = password
            user.reset_token = None
            db.session.commit()

            flash(
                'Password reset successful! You can now log in with your new password.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Password and Confirm Password do not match.', 'danger')

    return render_template('reset_password.html', token=token)


# สร้างโมเดล Site
class Site(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    url = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.Text)

# หน้าหลัก Manage Sites


@app.route('/manage-sites')
def manage_sites():
    sites = Site.query.all()
    return render_template('manage_sites.html', sites=sites)

# เพิ่ม Site


@app.route('/add-site', methods=['GET', 'POST'])
def add_site():
    if request.method == 'POST':
        name = request.form['name']
        url = request.form['url']
        description = request.form['description']

        new_site = Site(name=name, url=url, description=description)
        db.session.add(new_site)
        db.session.commit()
        flash('Site added successfully!', 'success')
        # เปลี่ยนเป็น URL ที่ต้องการให้กลับหลังจากเพิ่ม Site
        return redirect('/manage-sites')

    return render_template('add_site.html')

# แก้ไข Site


@app.route('/edit-site/<int:site_id>', methods=['GET', 'POST'])
def edit_site(site_id):
    site = Site.query.get(site_id)

    if request.method == 'POST':
        site.name = request.form['name']
        site.url = request.form['url']
        site.description = request.form['description']

        db.session.commit()
        flash('Site updated successfully!', 'success')
        # เปลี่ยนเป็น URL ที่ต้องการให้กลับหลังจากแก้ไข Site
        return redirect('/manage-sites')

    return render_template('edit_site.html', site=site)

# ลบ Site


@app.route('/remove-site/<int:site_id>', methods=['POST'])
def remove_site(site_id):
    site = Site.query.get(site_id)

    if site:
        db.session.delete(site)
        db.session.commit()
        flash('Site deleted successfully!', 'success')

    # เปลี่ยนเป็น URL ที่ต้องการให้กลับหลังจากลบ Site
    return redirect('/manage-sites')


@app.route('/delete-user', methods=['DELETE'])
def delete_user():
    data = request.get_json()
    username = data.get('username')

    # ค้นหาผู้ใช้ที่ต้องการลบจากฐานข้อมูล
    user = User.query.filter_by(username=username).first()

    if user:
        # ลบผู้ใช้
        db.session.delete(user)
        db.session.commit()
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})
# เพิ่ม route สำหรับส่งข้อมูลผู้ใช้


@app.route('/get_users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_data = [{'username': user.username} for user in users]
    return jsonify({'users': user_data})

# Function to authenticate user


def authenticate_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        return user
    return None

# Function to get user by ID


def get_user_by_id(user_id):
    return User.query.get(user_id)

# Function to update user information


def update_user(user, new_data):
    # Example: Update username, email, and is_admin
    user.username = new_data.get('username', user.username)
    user.email = new_data.get('email', user.email)
    user.is_admin = new_data.get('is_admin', user.is_admin)
    # Add more fields as needed

    db.session.commit()

# ตัวอย่างการใช้ฟังก์ชัน get_user_by_id ในการดึงข้อมูลผู้ใช้


@app.route('/profile')
def profile():
    user_id = session.get('user_id')
    if user_id:
        # ใช้ฟังก์ชัน get_user_by_id เพื่อดึงข้อมูลผู้ใช้โดยใช้ ID
        user = get_user_by_id(user_id)
        if user:
            return render_template('profile.html', user=user)
    return redirect(url_for('login'))
# ตัวอย่างการใช้ฟังก์ชัน update_user ในการอัพเดตข้อมูลผู้ใช้


@app.route('/update_profile', methods=['POST'])
def update_profile():
    user_id = session.get('user_id')
    if user_id:
        user = get_user_by_id(user_id)
        if user:
            new_data = {
                'username': request.form.get('username'),
                'email': request.form.get('email'),
                'is_admin': request.form.get('is_admin')
                # เพิ่มเติมตามต้องการ
            }
            # ใช้ฟังก์ชัน update_user เพื่ออัพเดตข้อมูลผู้ใช้
            update_user(user, new_data)
            flash('Profile updated successfully!', 'success')
    return redirect(url_for('profile'))




@app.route('/logout')
def logout():
    # ลบข้อมูล user_id ออกจาก session
    session.pop('user_id', None)
    
    # แสดงข้อความสำเร็จ
    flash('You have been logged out.', 'info')
    
    # ให้ผู้ใช้เดินทางกลับไปยังหน้าหลักหรือหน้า login
    return redirect(url_for('login.html'))  # แทน 'home' ด้วยชื่อฟังก์ชันหน้าหลักของคุณ
# หน้า Dashboard


@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        return render_template('dashboard.html', user=user)
    else:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('login'))


@app.route('/Home_Page')
def Home_Page():
    # ตัวอย่าง: ดึงข้อมูล user_id จาก session
    user_id = session.get('user_id')
    if user_id is None:
        # ถ้าไม่มี user_id ใน session แสดงว่าผู้ใช้ไม่ได้ลงชื่อเข้าใช้
        return redirect(url_for('login'))
    # ต่อไปนี้คุณสามารถใช้ user_id เพื่อดึงข้อมูลผู้ใช้หรือทำอย่างอื่นต่อไป
    total_users = User.query.count()
    return render_template('Home_Page.html', total_users=total_users)


@app.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html')


@app.route('/success')
def success():
    return 'Login successful!'


# ปรับแต่งให้ Flask app รันด้วย debug mode
if __name__ == '__main__':
    app.run(debug=True)
