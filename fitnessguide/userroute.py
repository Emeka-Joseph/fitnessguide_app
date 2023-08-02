import os,random
from datetime import datetime
from flask import render_template, redirect, flash, session, request, url_for
from fitnessguide.models import Users, Employment,Environment,Lifestyle,Personality,Relationship,Symptoms,Categories, Voucher,Readjustment,Sed_Lifestyle,Results,Contact
from fitnessguide import app, db
from fitnessguide.forms import LoginForm, SignUpForm, ContactForm
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import text
from sqlalchemy import desc,asc,or_,func

import string



def generate_name(): 
    filename = random.sample(string.ascii_lowercase,10) 
    return ''.join(filename)


@app.route('/')
def home():
    form=ContactForm()
    cid = session.get('loggedin')
    alluser = db.session.query(Users).filter(Users.user_id==cid).first()
    return render_template('users/index.html',form=form, alluser=alluser)


@app.route('/contact', methods=['GET','POST'])
def contact():
    form=ContactForm()
    if request.method == "GET":
        
        return render_template('users/index.html',form = form)
    else:
        name=request.form.get("username")
        mail=request.form.get("email")
        subject=request.form.get("subject")
        message=request.form.get("msg")
        if name !='' and mail != "" and subject !='' and message !='':
            new_msg = Contact(contact_name=name, contact_email=mail, contact_subject=subject, contact_content=message)
            db.session.add(new_msg)
            db.session.commit()
            flash("Thank you for reaching out, we will get back to you shortly", "success")
            return redirect('/')
        else:
            flash('You must fill the form correctly to send your request', "danger")
            return redirect('/')



@app.route('/signup', methods = ["GET", "POST"], strict_slashes = False)
def signup():
    form = SignUpForm()
    if request.method == "GET":
        #cid = session.get('loggedin')
        alluser = db.session.query(Users).all()
        
        return render_template('users/signup.html', title="Sign Up", form = form, alluser=alluser)
    else:
        fname = form.fname.data
        lname = form.lname.data
        email = form.email.data
        password=form.password.data
        conpassword = form.confirm_password.data
        hashed_password = generate_password_hash(password)
        checkmail = db.session.query(Users).filter(Users.user_email==email).first()
        if checkmail!=None:
            flash('there is already an account with that email, kindly sign in or verifie your details', 'warning')
            return redirect(url_for('signup'))
        else:
            if fname !='' and lname != "" and email !='' and password !='' and password==conpassword:
                new_user= Users(user_fname = fname, user_lname = lname, user_email = email,
                user_pwd = hashed_password, gender='',user_phone='',social_rs='',sed_ls='',sed_lie='')
                db.session.add(new_user)
                db.session.commit()
                userid = new_user.user_id
                session['loggedin']=userid
                flash(f"Account created for {form.fname.data}! Please proceed to LOGIN ", "success")
                return redirect(url_for('login'))
            else:
                flash('You must fill the form correctly to signup and check that your password matched', "danger")
                return redirect(url_for('signup'))

    


@app.route('/login', methods = (["GET", "POST"]), strict_slashes = False)
def login():
    form = LoginForm()
    if request.method=='GET':
        return render_template('users/login.html', title="Login", form=form)
    else:
        if form.validate_on_submit:
            email = form.email.data
            password = form.password.data
            #deets = db.session.query(Users).filter(Users.user_email==email).first()
            if email !="" and password !="":
                user = db.session.query(Users).filter(Users.user_email==email).first() 
                if user !=None:
                    pwd =user.user_pwd
                    chk = check_password_hash(pwd, password)
                    if chk:
                        id = user.user_id
                        session['loggedin'] = id
                        return redirect(url_for('home'))
                    else:
                        flash('Invalid email or password', "danger")
                        return redirect(url_for('login'))
                else:
                    flash("Ensure that your login details are correct, or signup to create an account", "danger")  
                    return redirect(url_for('login'))     
        else:
            flash("You must complete all fields", "danger")
            return redirect(url_for("signup"))

@app.route('/logout')
def user_logout():
    #pop the session redirect to home page
    if session.get('loggedin')!=None:
        session.pop('loggedin',None)
    return redirect(url_for('home'))

@app.route('/dashboard')
def user_dashboard():
    if session.get('loggedin')!=None:
        id = session['loggedin']
        deets = db.session.query(Users).get(id)
        return render_template('user/user_dashboard.html',deets=deets)



@app.route('/employment', methods=['GET','POST'])
def employment():
    #form=ContactForm()
    id = session.get('loggedin')
    if id ==None:
        flash('Please sign in to take the various categories of Evaluation Tests','warning')
        return redirect('/') 
    else:
        if request.method=='GET':
            user_deets = db.session.query(Users).filter(Users.user_id==id).first()
            deets = db.session.query(Results).all()
            return render_template('users/employment.html',user_deets=user_deets,deets=deets)
        else:
            em1 = int(request.form.get('q1',0))
            em2 = int(request.form.get('q2',0))
            em3 = int(request.form.get('q3',0))
            em4 = int(request.form.get('q4',0))
            em5 = int(request.form.get('q5',0))
            em6 = int(request.form.get('q6',0))
            em7 = int(request.form.get('q7',0))
            em8 = int(request.form.get('q8',0))
            em9 = int(request.form.get('q9',0))
            em10 =int(request.form.get('q10',0))
            em11 = int(request.form.get('q11',0))
            em12 = int(request.form.get('q12',0))
            em13 = int(request.form.get('q13',0))
            em14 = int(request.form.get('q14',0))
            em15 = int(request.form.get('q15',0))
            em16 = int(request.form.get('q16',0))
            
            resp = em1 + em2 + em3 + em4 + em5 + em6 + em7 + em8 + em9 + em10 + em11 + em12 + em13 + em14 + em15 + em16
            #res.employment=resp
            result = Results(employment=resp,environment='',lifestyle='',personality='',relationship='',symptoms='',social='',sed_life_hrs='',sed_life_conval='',user_id=id)
            db.session.add(result)
            db.session.commit()
            return redirect('/environment')
            

@app.route('/environment', methods=['GET','POST'])
def environment():
    id = session.get('loggedin')
    if id ==None:
        flash('Please sign in to take the various categories of Evaluation Tests','warning')
        return redirect('/') 
    else:
        if request.method=='GET':
            user_deets = db.session.query(Users).filter(Users.user_id==id).first()
            deets = db.session.query(Results).all()
            return render_template('users/environment.html',user_deets=user_deets,deets=deets)
        else:
            en1 = int(request.form.get('q1',0))
            en2 = int(request.form.get('q2',0))
            en3 = int(request.form.get('q3',0))
            en4 = int(request.form.get('q4',0))
            en5 = int(request.form.get('q5',0))
            en6 = int(request.form.get('q6',0))
            en7 = int(request.form.get('q7',0))
            en8 = int(request.form.get('q8',0))
            en9 = int(request.form.get('q9',0))
            en10 = int(request.form.get('q10',0))
            en11 = int(request.form.get('q11',0))
            en12 = int(request.form.get('q12',0))
            en13 = int(request.form.get('q13',0))
            en14 = int(request.form.get('q14',0))
            en15 = int(request.form.get('q15',0))
            en16 = int(request.form.get('q16',0))
            
            resp = en1 + en2 + en3 + en4 + en5 + en6 + en7 + en8 + en9 + en10 + en11 + en12 + en13 + en14 + en15 + en16

            res = db.session.query(Results).first()    
            rezz = Results.query.order_by(Results.res_sl_id.desc()).first()  
            rezz.environment=resp
            db.session.commit()
        return redirect(url_for('lifestyle'))


@app.route('/lifestyle', methods=['GET','POST'])
def lifestyle():
    id = session.get('loggedin')
    if id ==None:
        flash('Please sign in to take the various categories of Evaluation Tests','warning')
        return redirect('/') 
    else:
        if request.method=='GET':
            user_deets = db.session.query(Users).filter(Users.user_id==id).first()
            deets = db.session.query(Results).all()
            return render_template('users/lifestyle.html',user_deets=user_deets,deets=deets)
        else:
            ls1 = int(request.form.get('q1',0))
            ls2 = int(request.form.get('q2',0))
            ls3 = int(request.form.get('q3',0))
            ls4 = int(request.form.get('q4',0))
            ls5 = int(request.form.get('q5',0))
            ls6 = int(request.form.get('q6',0))
            ls7 = int(request.form.get('q7',0))
            ls8 = int(request.form.get('q8',0))
            ls9 = int(request.form.get('q9',0))
            ls10 = int(request.form.get('q10',0))
            ls11 = int(request.form.get('q11',0))
            ls12 = int(request.form.get('q12',0))
            ls13 = int(request.form.get('q13',0))
            ls14 = int(request.form.get('q14',0))
            ls15 = int(request.form.get('q15',0))
            ls16 = int(request.form.get('q16',0))

            resp = ls1 + ls2 + ls3 + ls4 + ls5 + ls6 + ls7 + ls8 + ls9 + ls10 + ls11 + ls12 + ls13 + ls14 + ls15 + ls16
            rezz = Results.query.order_by(Results.res_sl_id.desc()).first() 
            rezz.lifestyle=resp
            db.session.commit()
            return redirect(url_for('personality'))



@app.route('/personality', methods=['GET','POST'])
def personality():
    id = session.get('loggedin')
    if id ==None:
        flash('Please sign in to take the various categories of Evaluation Tests','warning')
        return redirect('/') 
    else:
        if request.method=='GET':
            user_deets = db.session.query(Users).filter(Users.user_id==id).first()
            deets = db.session.query(Results).all()
            return render_template('users/personality.html',user_deets=user_deets,deets=deets)
        else:
            p1 = int(request.form.get('q1',0))
            p2 = int(request.form.get('q2',0))
            p3 = int(request.form.get('q3',0))
            p4 = int(request.form.get('q4',0))
            p5 = int(request.form.get('q5',0))
            p6 = int(request.form.get('q6',0))
            p7 = int(request.form.get('q7',0))
            p8 = int(request.form.get('q8',0))
            p9 = int(request.form.get('q9',0))
            p10 = int(request.form.get('q10',0))
            p11 = int(request.form.get('q11',0))
            p12 = int(request.form.get('q12',0))
            p13 = int(request.form.get('q13',0))
            p14 = int(request.form.get('q14',0))
            p15 = int(request.form.get('q15',0))
            p16 = int(request.form.get('q16',0))
            p17 = int(request.form.get('q17',0))
            p18 = int(request.form.get('q18',0))
            p19 = int(request.form.get('q19',0))
            p20 = int(request.form.get('q20',0))


            resp = p1 + p2 + p3 + p4 + p5 + p6 + p7 + p8 + p9 + p10 + p11 + p12 + p13 + p14 + p15 + p16 + p17 + p18 + p19 + p20
            rezz = Results.query.order_by(Results.res_sl_id.desc()).first() 
            rezz.personality=resp
            db.session.commit()
            return redirect(url_for('relationship'))


@app.route('/relationship', methods=['GET','POST'])
def relationship():
    id = session.get('loggedin')
    if id ==None:
        flash('Please sign in to take the various categories of Evaluation Tests','warning')
        return redirect('/') 
    else:
        if request.method=='GET':
            user_deets = db.session.query(Users).filter(Users.user_id==id).first()
            deets = db.session.query(Results).all()
            return render_template('users/relationship.html',user_deets=user_deets,deets=deets)
        else:
            r1 = int(request.form.get('q1',0))
            r2 = int(request.form.get('q2',0))
            r3 = int(request.form.get('q3',0))
            r4 = int(request.form.get('q4',0))
            r5 = int(request.form.get('q5',0))
            r6 = int(request.form.get('q6',0))
            r7 = int(request.form.get('q7',0))
            r8 = int(request.form.get('q8',0))
            r9 = int(request.form.get('q9',0))
            r10 = int(request.form.get('q10',0))
            r11 = int(request.form.get('q11',0))
            r12 = int(request.form.get('q12',0))
            r13 = int(request.form.get('q13',0))
            r14 = int(request.form.get('q14',0))
            r15 = int(request.form.get('q15',0))
            r16 = int(request.form.get('q16',0))

            resp = r1 + r2 + r3 + r4 + r5 + r6 + r7 + r8 + r9 + r10 + r11 + r12 + r13 + r14 + r15 + r16
            rezz = Results.query.order_by(Results.res_sl_id.desc()).first() 
            rezz.relationship=resp
            db.session.commit()
            return redirect(url_for('symptoms'))


@app.route('/symptoms', methods=['GET','POST'])
def symptoms():
    id = session.get('loggedin')
    if id ==None:
        flash('Please sign in to take the various categories of Evaluation Tests','warning')
        return redirect('/') 
    else:
        if request.method=='GET':
            user_deets = db.session.query(Users).filter(Users.user_id==id).first()
            deets = db.session.query(Results).all()
            return render_template('users/symptoms.html',user_deets=user_deets,deets=deets)
        else:
            s1 = int(request.form.get('q1',0))
            s2 = int(request.form.get('q2',0))
            s3 = int(request.form.get('q3',0))
            s4 = int(request.form.get('q4',0))
            s5 = int(request.form.get('q5',0))
            s6 = int(request.form.get('q6',0))
            s7 = int(request.form.get('q7',0))
            s8 = int(request.form.get('q8',0))
            s9 = int(request.form.get('q9',0))
            s10 = int(request.form.get('q10',0))
            s11 = int(request.form.get('q11',0))
            s12 = int(request.form.get('q12',0))
            s13 = int(request.form.get('q13',0))
            s14 = int(request.form.get('q14',0))
            s15 = int(request.form.get('q15',0))
            s16 = int(request.form.get('q16',0))

            resp = s1 + s2 + s3 + s4 + s5 + s6 + s7 + s8 + s9 + s10 + s11 + s12 + s13 + s14 + s15 + s16
            rezz = Results.query.order_by(Results.res_sl_id.desc()).first() 
            rezz.symptoms=resp
            db.session.commit()
            return redirect(url_for('step2'))


@app.route('/result', methods=['GET','POST'])
def result():
    if session.get('loggedin') ==None:
        flash('Please sign in to view result','warning')
        return redirect('/') 
    else:
        id = session['loggedin']
        allresults = Results.query.order_by(desc(Results.user_id)).all()
        pfie = Results.query.order_by(Results.res_sl_id.desc()).first() 
        mdeets = Users.query.order_by(Users.user_id).all()
        userdeets = db.session.query(Users).get(id)
        sed_total = pfie.employment + pfie.environment + pfie.lifestyle + pfie.personality + pfie.relationship + pfie.symptoms 
        if request.method=='GET':
            allresults = Results.query.order_by(desc(Results.user_id)).all()
            return render_template('users/result.html', pfie=pfie,mdeets=mdeets,sed_total=sed_total,id=id,userdeets=userdeets,allresults=allresults)


@app.route('/result_sed', methods=['GET','POST'])
def result_sed():
    if session.get('loggedin') ==None:
        flash('Please sign in to take the various categories of Evaluation Tests','warning')
        return redirect('/') 
    else:
        id = session['loggedin']
        pfie = Results.query.order_by(Results.res_sl_id.desc()).first() 
        mdeets = Users.query.order_by(Users.user_id).all()
        userdeets = db.session.query(Users).get(id)
        total = pfie.sed_life_conval 
        if request.method=='GET':
            return render_template('users/result_sedlife.html', pfie=pfie,mdeets=mdeets,total=total,id=id,userdeets=userdeets)



@app.route('/result_social', methods=['GET','POST'])
def result_social():
    if session.get('loggedin') ==None:
        flash('Please sign in to take the various categories of Evaluation Tests','warning')
        return redirect('/') 
    else:
        id = session['loggedin']
        pfie = Results.query.order_by(Results.res_sl_id.desc()).first() 
        mdeets = Users.query.order_by(Users.user_id).all()
        userdeets = db.session.query(Users).get(id)
        total = pfie.social 
        if request.method=='GET':
            return render_template('users/result_social.html', pfie=pfie,mdeets=mdeets,total=total,id=id,userdeets=userdeets)

   

@app.route('/print_result1')
def print_result1():
    if session.get('loggedin') ==None:
        flash('Please sign in to take the various categories of Evaluation Tests','warning')
        return redirect('/')
    else:
        id = session.get('loggedin')
        allresults = Results.query.order_by(desc(Results.user_id)).first()        
        pfie = Results.query.order_by(Results.res_sl_id.desc()).first() 

        deets = pfie.employment + pfie.environment + pfie.lifestyle + pfie.personality + pfie.relationship + pfie.symptoms

        return render_template('users/print_result1.html', allresults=allresults, deets=deets)


@app.route('/step2', methods=['GET','POST'])
def step2():
    id = session.get('loggedin')
    if id ==None:
        flash('Please sign in to take the various categories of Evaluation Tests','warning')
        return redirect('/') 
    else:
        if request.method=='GET':
            user_deets = db.session.query(Users).filter(Users.user_id==id).first()
            deets = db.session.query(Results).all()
            return render_template('users/step2.html',user_deets=user_deets,deets=deets)
        else:
            s1 = request.form.get('q1')
            s2 = request.form.get('q2')
            s3 = request.form.get('q3')
            s4 = request.form.get('q4')
            s5 = request.form.get('q5')
            if s1=='yes' or s2=='yes' or  s3=='yes' or s4=='yes' or s5=='yes':
                m = 3
                rezz = Results.query.order_by(Results.res_sl_id.desc()).first() 
                rezz.symptoms=rezz.symptoms + 3
                db.session.commit()
                return redirect(url_for('step3'))


@app.route('/step3', methods=['GET','POST'])
def step3():
    id = session.get('loggedin')
    if id ==None:
        flash('Please sign in to take the various categories of Evaluation Tests','warning')
        return redirect('/') 
    else:
        if request.method=='GET':
            user_deets = db.session.query(Users).filter(Users.user_id==id).first()
            deets = db.session.query(Results).all()
            return render_template('users/step3.html',user_deets=user_deets,deets=deets)
        else:
            s1 = request.form.get('q1')
            s2 = request.form.get('q2')
            s3 = request.form.get('q3')
            s4 = request.form.get('q4')
            s5 = request.form.get('q5')

            if s1=='yes' or s2=='yes' or  s3=='yes' or s4=='yes' or s5=='yes':
                rezz = Results.query.order_by(Results.res_sl_id.desc()).first() 
                rezz.symptoms=rezz.symptoms + 2
                db.session.commit()
                return redirect(url_for('result'))


@app.route('/sed_lifestyle', methods=['GET','POST'])
def sed_lifestyle():
    id = session.get('loggedin')
    if id ==None:
        flash('Please sign in to take the various categories of Evaluation Tests','warning')
        return redirect('/') 
    else:
        if request.method=='GET':
            user_deets = db.session.query(Users).filter(Users.user_id==id).first()
            deets = db.session.query(Results).all()
            return render_template('users/sedentary_lifestyle.html',user_deets=user_deets,deets=deets)
        else:
            slt1 = float(request.form.get('sl1',0.0))
            slt2 = float(request.form.get('sl2',0.0))
            slt3 = float(request.form.get('sl3',0.0))
            slt4 = float(request.form.get('sl4',0.0))
            slt5 = float(request.form.get('sl5',0.0))
            slt6 = float(request.form.get('sl6',0.0))
            slt7 = float(request.form.get('sl7',0.0))
            slt8 = float(request.form.get('sl8',0.0))
            slt9 = float(request.form.get('sl9',0.0))
            slt10 = float(request.form.get('sl10',0.0))
            slt11 = float(request.form.get('sl11',0.0))
            slt12 = float(request.form.get('sl12',0.0))
            slt13 = float(request.form.get('sl13',0.0))
            slt14 = float(request.form.get('sl14',0.0))
            slt15 = float(request.form.get('sl15',0.0))
            slt16 = float(request.form.get('sl16',0.0))
            slt17 = float(request.form.get('sl17',0.0))

            if slt1=='' or slt2=='' or slt3=='' or slt4=='' or slt5=='' or slt6=='' or slt7=='' or slt8=='' or slt9=='' or slt10=='' or slt11=='' or slt12=='' or slt13=='' or slt14=='' or slt15=='' or slt16=='' or slt17=='':
                flash('Kindly fill all the fields ','danger')
                return render_template('users/sedentary_lifestyle.html')
            else:
                resp = slt1 + slt2 + slt3 + slt4 + slt5 + slt6 + slt7 + slt8 + slt9 + slt10 + slt11 + slt12 + slt13 + slt14 + slt15 + slt16 + slt17

                if resp >24:
                    flash('Kindly review your input for you cannot have more than 24 hours in a day','danger')
                    return render_template('users/sedentary_lifestyle.html')
                else:
                    conval = slt1*0.8 + slt2*0.8 + slt3*1.5 + slt4*1.5 + slt5*1.5 + slt6*1.5 + slt7*1.5 + slt8*2 + slt9*3 + slt10*4 + slt11*5 + slt12*3 + slt13*4 + slt14*5 + slt15*7 + slt16*8 + slt17*9

                    rezz = Results.query.order_by(Results.res_sl_id.desc()).first() 
                    rezz.sed_life_hrs=resp
                    rezz.sed_life_conval=conval
                    
                    db.session.commit()
                    return redirect(url_for('result_sed'))


@app.route('/payment')
def payment():
    cid = session.get('loggedin')
    deets = db.session.query(Users).filter(Users.user_id==cid).first()
    alluser = db.session.query(Users).filter(Users.user_id==cid).first()
    return render_template('users/payment.html',deets=deets, alluser=alluser)

@app.route('/social', methods=['GET','POST'])
def social():
    id = session.get('loggedin')
    if id ==None:
        flash('Please sign in to take the various categories of Evaluation Tests','warning')
        return redirect('/') 
    else:
        if request.method=='GET':
            user_deets = db.session.query(Users).filter(Users.user_id==id).first()
            deets = db.session.query(Results).all()
            return render_template('users/social.html',user_deets=user_deets,deets=deets)
        else:
            int(request.form.get('dos1', 0))
            
            soc1 = int(request.form.get('dos1',0))
            soc2 = int(request.form.get('dos2',0))
            soc3 = int(request.form.get('dos3',0))
            soc4 = int(request.form.get('dos4',0))
            soc5 = int(request.form.get('dos5',0))
            soc6 = int(request.form.get('dos6',0))
            soc7 = int(request.form.get('dos7',0))
            soc8 = int(request.form.get('dos8',0))
            soc9 = int(request.form.get('dos9',0))
            soc10 = int(request.form.get('dos10',0))
            soc11 = int(request.form.get('dos11',0))
            soc12 = int(request.form.get('dos12',0))
            soc13 = int(request.form.get('dos13',0))
            soc14 = int(request.form.get('dos14',0))
            soc15 = int(request.form.get('dos15',0))
            soc16 = int(request.form.get('dos16',0))
            soc17 = int(request.form.get('dos17',0))
            soc18 = int(request.form.get('dos18',0))
            soc19 = int(request.form.get('dos19',0))
            soc20 = int(request.form.get('dos20',0))
            soc21 = int(request.form.get('dos21',0))
            soc22 = int(request.form.get('dos22',0))
            soc23 = int(request.form.get('dos23',0))
            soc24 = int(request.form.get('dos24',0))
            soc25 = int(request.form.get('dos25',0))
            soc26 = int(request.form.get('dos26',0))
            soc27 = int(request.form.get('dos27',0))
            soc28 = int(request.form.get('dos28',0))
            soc29 = int(request.form.get('dos29',0))
            soc30 = int(request.form.get('dos30',0))
            soc31 = int(request.form.get('dos31',0))
            soc32 = int(request.form.get('dos32',0))
            soc33 = int(request.form.get('dos33',0))
            soc34 = int(request.form.get('dos34',0))
            soc35 = int(request.form.get('dos35',0))
            soc36 = int(request.form.get('dos36',0))
            soc37 = int(request.form.get('dos37',0))
            soc38 = int(request.form.get('dos38',0))
            soc39 = int(request.form.get('dos39',0))
            soc40 = int(request.form.get('dos40',0))
            soc41 = int(request.form.get('dos41',0))
            soc42 = int(request.form.get('dos42',0))
            soc43 = int(request.form.get('dos43',0))
            soc44 = int(request.form.get('dos44',0))

            resp = soc1 + soc2 + soc3 + soc4 + soc5 + soc6 + soc7 + soc8 + soc9 + soc10 + soc11 + soc12 + soc13 + soc14 + soc15 + soc16 + soc17 + soc18 + soc19 + soc20 + soc21 + soc22 + soc23 + soc24 + soc25 + soc26 + soc27 + soc28 + soc29 + soc30 + soc31 + soc32 + soc33 + soc34 + soc35 + soc36 + soc37 + soc38 + soc39 + soc40 + soc41 + soc42 + soc43 + soc44
            rezz = Results.query.order_by(Results.res_sl_id.desc()).first() 
            rezz.social=resp
            db.session.commit()
            return redirect(url_for('result_social'))

        
