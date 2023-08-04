import os,random
from flask import render_template, redirect, flash, session, request, url_for
from fitnessguide.models import Admin,Users, Voucher,Payment,Results,Contact
from fitnessguide import app, db
from fitnessguide.forms import AdminLoginForm
from sqlalchemy.sql import text
from sqlalchemy import desc,asc,or_,func
from datetime import datetime
import string

def generate():
    return ''.join(random.choices(string.digits, k=15))


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
    return redirect(url_for('manage_payment'))


@app.route('/AdminLogin', methods = (["GET", "POST"]), strict_slashes = False)
def AdminLogin():
    form = AdminLoginForm()
    if request.method=='GET':
        return render_template('admin/login.html', title="Admin Login", form=form)
    else:
        if form.validate_on_submit:
            email = form.email.data
            password = form.password.data
            if email !="" and password !="":
                admin = db.session.query(Admin).filter(Admin.admin_email==email).first() 
                if admin !=None:
                    pwd =admin.admin_password
                    chk = db.session.query(Admin).filter(Admin.admin_password==password).first()
                    if chk:
                        id = admin.admin_id
                        session['Administrator'] = id
                        return redirect(url_for('admin_index'))
                    else:
                        flash('Invalid email or password', "danger")
                        return redirect(url_for('AdminLogin'))
                else:
                    flash("Ensure that your login details are correct, or signup to create an account", "danger")  
                    return redirect(url_for('AdminLogin'))     
        else:
            flash("You must complete all fields", "danger")
            return redirect(url_for("AdminLogin"))



@app.route('/admin_index')
def admin_index():
   
    id = session.get('Administrator')
    if id ==None:
        flash('Please sign in as the Admin','warning')
        return redirect('/AdminLogin') 
    else:
        allusers = db.session.query(Users).all()
        allresults = db.session.query(Results).all()
        pool = db.session.query(func.sum(Users.user_id)).scalar()
        allpayment = db.session.query(func.sum(Payment.pay_amount)).scalar()
        real_admin = db.session.query(Admin).filter(Admin.admin_id==id).first()
        allmessages = db.session.query(Contact).all()
        return render_template('admin/admin_index.html',allusers=allusers,allresults=allresults,pool=pool,allmessages=allmessages,allpayment=allpayment,real_admin=real_admin)

@app.route('/manage_users')
def manage_users():
    id = session.get('Administrator')
    if id ==None:
        flash('Please sign in as the Admin','warning')
        return redirect('/AdminLogin') 
    else:
        allusers = db.session.query(Users).all()
        allresults = db.session.query(Results).all()
        return render_template('admin/manage_users.html',allusers=allusers,allresults=allresults)


@app.route('/manage_results')
def manage_results():
    id = session.get('Administrator')
    if id ==None:
        flash('Please sign in as the Admin','warning')
        return redirect('/AdminLogin') 
    else:
        allusers = db.session.query(Users).all()
        allresults = db.session.query(Results).all()
        return render_template('admin/manage_results.html',allusers=allusers,allresults=allresults)


@app.route('/manage_payment')
def manage_payment():
    id = session.get('Administrator')
    if id ==None:
        flash('Please sign in as the Admin','warning')
        return redirect('/AdminLogin') 
    else:
        allusers = db.session.query(Users).all()
        allresults = db.session.query(Results).all()
        allvouchers = db.session.query(Voucher).all()
        deets = db.session.query(Payment).all()
        return render_template('admin/manage_payment.html',allusers=allusers,allresults=allresults,allvouchers=allvouchers,deets=deets)



@app.route('/manage_messages')
def manage_messages():
    id = session.get('Administrator')
    if id ==None:
        flash('Please sign in as the Admin','warning')
        return redirect('/AdminLogin') 
    else:
        allusers = db.session.query(Users).all()
        allmessages = db.session.query(Contact).all()
        return render_template('admin/manage_messages.html',allusers=allusers,allmessages=allmessages)


@app.route('/delete/<int:id>')
def delete(id): 
    allusers=db.session.query(Users).all()
    user_to_del=Users.query.get_or_404(id)
    userobj =   Users.query.get_or_404(id)
    try:
        db.session.delete(userobj)
        db.session.commit()
        flash('user deleted successfully')
        deet_user = Users.query.order_by(Users.user_id) 
        return redirect(url_for('admin_index'))
        
    except:
        flash('whoops, there was a problem deleting the user')
        return redirect(url_for('admin_index'))
    


@app.route('/adminlogout')
def admin_logout():
    #pop the session redirect to home page
    if session.get('Administrator')!=None:
        session.pop('Administrator',None)
    return redirect(url_for('AdminLogin'))