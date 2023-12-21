# # forms.py
# # โมดูลที่ประกอบไปด้วยคลาสฟอร์มสำหรับการลงชื่อเข้าใช้, การลงทะเบียน, และการแก้ไขผู้ใช้

# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, SubmitField
# from wtforms.validators import DataRequired, Email, EqualTo, Length


# class LoginForm(FlaskForm):
#     username = StringField('Username', validators=[DataRequired()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     submit = SubmitField('Login')


# class RegisterForm(FlaskForm):
#     username = StringField('Username', validators=[DataRequired()])
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     # รหัสผ่านควรมีความยาวอย่างน้อย 6 ตัว
#     password = PasswordField('Password', validators=[
#                              DataRequired(), Length(min=6)])
#     confirm_password = PasswordField('Confirm Password', validators=[
#                                      DataRequired(), EqualTo('password')])
#     submit = SubmitField('Register')


# class EditUserForm(FlaskForm):
#     username = StringField('Username', validators=[DataRequired()])
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     # ตรวจสอบหน้าที่ว่าเป็น 'user' หรือ 'admin'
#     is_admin = StringField('Role', validators=[DataRequired()])
#     # รหัสผ่านควรมีความยาวอย่างน้อย 6 ตัว
#     password = PasswordField('New Password', validators=[Length(min=6)])
#     submit = SubmitField('Update')
