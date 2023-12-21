# from flask_sqlalchemy import SQLAlchemy

# # สร้างอ็อบเจ็กต์ SQLAlchemy
# db = SQLAlchemy()

# # ประกาศโมเดล User


# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(100), unique=True, nullable=False)
#     email = db.Column(db.String(100), unique=True, nullable=False)
#     password = db.Column(db.String(100), nullable=False)
#     is_admin = db.Column(db.Boolean, default=False)
#     # เพิ่มเติมตามต้องการ

# # ประกาศโมเดล AMR_REGION


# class AMR_REGION(db.Model):
#     PL_REGION_ID = db.Column(db.String(10), primary_key=True)
#     # เพิ่มคอลัมน์ตามต้องการ

# # ประกาศโมเดล AMR_FIELD_ID


# class AMR_FIELD_ID(db.Model):
#     FIELD_ID = db.Column(db.Integer, primary_key=True)
#     TAG_ID = db.Column(db.String(10), nullable=True)
#     METER_ID = db.Column(db.String(20), nullable=True)
#     # เพิ่มคอลัมน์ตามต้องการ

# # ประกาศโมเดล AMR_PL_GROUP


# class AMR_PL_GROUP(db.Model):
#     PL_REGION_ID = db.Column(db.String(10), primary_key=True)
#     FIELD_ID = db.Column(db.Integer, nullable=True)
#     # เพิ่มคอลัมน์ตามต้องการ

# # ประกาศโมเดล AMR_BILLING_DATA


# class AMR_BILLING_DATA(db.Model):
#     METER_ID = db.Column(db.String(20), primary_key=True)
#     DATA_DATE = db.Column(db.String(10), nullable=True)
#     CORRECTED_VOL = db.Column(db.Float, nullable=True)
#     UNCORRECTED_VOL = db.Column(db.Float, nullable=True)
#     AVR_PF = db.Column(db.Float, nullable=True)
#     AVR_TF = db.Column(db.Float, nullable=True)
#     # เพิ่มคอลัมน์ตามต้องการ

# # ไม่จำเป็นต้องมี db.create_all() ที่นี่ เนื่องจากแบบแผนของเราคือสร้างฐานข้อมูลในไฟล์ Flask app หลัก
