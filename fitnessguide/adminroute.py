import os,random
from flask import render_template, redirect, flash, session, request, url_for
from fitnessguide.models import Users, Employment,Environment,Lifestyle,Personality,Relationship,Symptoms,Categories, Voucher, Readjustment,Sed_Lifestyle,Results,Contact
from fitnessguide import app, db
from fitnessguide.forms import LoginForm, SignUpForm, ContactForm
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import text
from sqlalchemy import desc,asc,or_,func

from datetime import datetime



import string

def generate():
    return ''.join(random.choices(string.digits, k=15))



def generate_name(): 
    filename = random.sample(String.ascii_lowercase,10) 
    return ''.join(filename)


def generate():
    while True:
        voucher_code = ''.join(random.choices(string.digits, k=15))
        # Check if the generated code already exists in the database
        existing_voucher = Voucher.query.filter_by(voucher_code=voucher_code).first()

        if not existing_voucher:
            return voucher_code


@app.route('/generate_voucher', methods=['POST'])
def generate_voucher():
    if request.method == 'POST':
        for _ in range(20):  # Replace 10 with the number of voucher codes you want to generate.
            voucher_code = generate()
            date = datetime.now()

            # Insert the generated voucher code and date into the database using ORM
            voucher = Voucher(voucher_code=voucher_code, date=date)
            db.session.add(voucher)
            db.session.commit()

    #return render_template('admin/admin_index.html')
    return redirect(url_for('manage_payment'))


'''@app.route('/generate_voucher', methods=['POST'])
def generate_voucher():
    if request.method == 'POST':
        for _ in range(10):  # Replace 10 with the number of voucher codes you want to generate.
            voucher_code = generate()
            date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # Insert the generated voucher code and date into the database using ORM (Assuming you have a 'Voucher' model defined)
            voucher = Voucher(voucher_code=voucher_code, date=date)
            db.session.add(voucher)
            db.session.commit()

    return redirect('/') 
'''

@app.route('/admin_dashboard')
def admin_dashboard():
    allusers = db.session.query(Users).all()
    allresults = db.session.query(Results).all()
    allvouchers = db.sesison.query(Voucher).all()
    return render_template('admin/admin_dashboard.html',allusers=allusers,allresults=allresults,allvouchers=allvouchers)

@app.route('/admin_index')
def admin_index():
    allusers = db.session.query(Users).all()
    allresults = db.session.query(Results).all()
    return render_template('admin/admin_index.html',allusers=allusers,allresults=allresults)

@app.route('/manage_users')
def manage_users():
    allusers = db.session.query(Users).all()
    allresults = db.session.query(Results).all()
    return render_template('admin/manage_users.html',allusers=allusers,allresults=allresults)




@app.route('/manage_results')
def manage_results():
    allusers = db.session.query(Users).all()
    allresults = db.session.query(Results).all()
    return render_template('admin/manage_results.html',allusers=allusers,allresults=allresults)


@app.route('/manage_payment')
def manage_payment():
    allusers = db.session.query(Users).all()
    allresults = db.session.query(Results).all()
    allvouchers = db.session.query(Voucher).all()
    return render_template('admin/manage_payment.html',allusers=allusers,allresults=allresults,allvouchers=allvouchers)