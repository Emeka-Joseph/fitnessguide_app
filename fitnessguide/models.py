from datetime import datetime
from fitnessguide import db 


class Users(db.Model):
    user_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    user_fname = db.Column(db.String(100),nullable=False)
    user_lname = db.Column(db.String(100),nullable=False)
    user_email = db.Column(db.String(120), unique=True) 
    user_datereg=db.Column(db.DateTime(), default=datetime.utcnow)
    user_pwd=db.Column(db.String(120),nullable=False)
    

class Admin(db.Model):
    admin_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    admin_fullname = db.Column(db.String(100),nullable=False)
    admin_email = db.Column(db.String(120)) 
    admin_password=db.Column(db.String(120),nullable=False)


class Payment(db.Model):
    pay_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    pay_date = db.Column(db.DateTime(),default=datetime.utcnow)
    pay_amount = db.Column(db.Integer)
    pay_name = db.Column(db.String(120), nullable=False)
    narration = db.Column(db.String(255),nullable=False)
    pay_pop = db.Column(db.String(120), nullable=False)
    pay_userid = db.Column(db.Integer,db.ForeignKey('users.user_id'), nullable=True)


class Voucher(db.Model):
    voucher_id = db.Column(db.Integer, primary_key=True)
    voucher_code = db.Column(db.String(15), unique=True, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    voucher_userid = db.Column(db.String(150),nullable=True)

class Results(db.Model):
    res_sl_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    order_by = db.desc(res_sl_id)
    employment = db.Column(db.Integer,nullable=True)
    environment = db.Column(db.Integer,nullable=True)
    lifestyle = db.Column(db.Integer,nullable=True)
    personality = db.Column(db.Integer,nullable=True)
    relationship = db.Column(db.Integer,nullable=True)
    symptoms = db.Column(db.Integer,nullable=True)
    social = db.Column(db.Integer,nullable=True)
    sed_life_hrs = db.Column(db.Float,nullable=True)
    sed_life_conval = db.Column(db.Float,nullable=True)
    date = db.Column(db.DateTime(),default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),nullable=True)


class Contact(db.Model):
    contact_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    contact_email = db.Column(db.String(100),nullable=False)
    contact_name =db.Column(db.String(255),nullable=True)
    contact_subject = db.Column(db.String(80),nullable=True)
    contact_content = db.Column(db.String(255), nullable=True)


    
