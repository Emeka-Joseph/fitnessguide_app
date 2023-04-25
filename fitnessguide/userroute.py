import os,random
from flask import render_template, redirect, flash, session, request, url_for
from fitnessguide.models import Users, Employment,Environment,Lifestyle,Personality,Relationship,Symptoms,Categories,Readjustment,Sed_Lifestyle,Results,Contact
from fitnessguide import app, db
from fitnessguide.forms import LoginForm, SignUpForm, ContactForm
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import text
from sqlalchemy import desc,asc,or_,func


def generate_name(): 
    filename = random.sample(string.ascii_lowercase,10) 
    return ''.join(filename)

@app.route('/')
def home():
    form=ContactForm()
    return render_template('users/index.html',form=form)


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
        return render_template('users/signup.html', title="Sign Up", form = form)
    else:
        fname = form.fname.data
        lname = form.lname.data
        email = form.email.data
        password=form.password.data
        conpassword = form.confirm_password.data
        hashed_password = generate_password_hash(password)
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
        
        #mdeets = db.session.query(Employment).order_by(Employment.q_id).all()
        #cid = db.session.query(Employment).order_by(Employment.q_id).first()
        if request.method=='GET':
            user_deets = db.session.query(Users).filter(Users.user_id==id).first()
            deets = db.session.query(Results).all()
            return render_template('users/employment.html',user_deets=user_deets,deets=deets)
        else:
            em1 = request.form.get('q1')
            em2 = request.form.get('q2')
            em3 = request.form.get('q3')
            em4 = request.form.get('q4')
            em5 = request.form.get('q5')
            em6 = request.form.get('q6')
            em7 = request.form.get('q7')
            em8 = request.form.get('q8')
            em9 = request.form.get('q9')
            em10 = request.form.get('q10')
            em11 = request.form.get('q11')
            em12 = request.form.get('q12')
            em13 = request.form.get('q13')
            em14 = request.form.get('q14')
            em15 = request.form.get('q15')
            em16 = request.form.get('q16')

            #res = db.session.query(Results).order_by(Results.res_sl_id.desc()).first()  
            

            #mdeets = db.session.query(Results).filter(Results.user_id==res).first()
            resp = int(em1) + int(em2) + int(em3) + int(em4) + int(em5) + int(em6) + int(em7) + int(em8) + int(em9) + int(em10) + int(em11) + int(em12) + int(em13) + int(em14) + int(em15) + int(em16)
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
            en1 = request.form.get('q1')
            en2 = request.form.get('q2')
            en3 = request.form.get('q3')
            en4 = request.form.get('q4')
            en5 = request.form.get('q5')
            en6 = request.form.get('q6')
            en7 = request.form.get('q7')
            en8 = request.form.get('q8')
            en9 = request.form.get('q9')
            en10 = request.form.get('q10')
            en11 = request.form.get('q11')
            en12 = request.form.get('q12')
            en13 = request.form.get('q13')
            en14 = request.form.get('q14')
            en15 = request.form.get('q15')
            en16 = request.form.get('q16')
            
            resp = int(en1) + int(en2) + int(en3) + int(en4) + int(en5) + int(en6) + int(en7) + int(en8) + int(en9) + int(en10) + int(en11) + int(en12) + int(en13) + int(en14) + int(en15) + int(en16)

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
            ls1 = request.form.get('q1')
            ls2 = request.form.get('q2')
            ls3 = request.form.get('q3')
            ls4 = request.form.get('q4')
            ls5 = request.form.get('q5')
            ls6 = request.form.get('q6')
            ls7 = request.form.get('q7')
            ls8 = request.form.get('q8')
            ls9 = request.form.get('q9')
            ls10 = request.form.get('q10')
            ls11 = request.form.get('q11')
            ls12 = request.form.get('q12')
            ls13 = request.form.get('q13')
            ls14 = request.form.get('q14')
            ls15 = request.form.get('q15')
            ls16 = request.form.get('q16')

            resp = int(ls1) + int(ls2) + int(ls3) + int(ls4) + int(ls5) + int(ls6) + int(ls7) + int(ls8) + int(ls9) + int(ls10) + int(ls11) + int(ls12) + int(ls13) + int(ls14) + int(ls15) + int(ls16)
            rezz = Results.query.order_by(Results.res_sl_id.desc()).first() 
            rezz.personality=resp
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
            p1 = request.form.get('q1')
            p2 = request.form.get('q2')
            p3 = request.form.get('q3')
            p4 = request.form.get('q4')
            p5 = request.form.get('q5')
            p6 = request.form.get('q6')
            p7 = request.form.get('q7')
            p8 = request.form.get('q8')
            p9 = request.form.get('q9')
            p10 = request.form.get('q10')
            p11 = request.form.get('q11')
            p12 = request.form.get('q12')
            p13 = request.form.get('q13')
            p14 = request.form.get('q14')
            p15 = request.form.get('q15')
            p16 = request.form.get('q16')
            p17 = request.form.get('q17')
            p18 = request.form.get('q18')
            p19 = request.form.get('q19')
            p20 = request.form.get('q20')


            resp = int(p1) + int(p2) + int(p3) + int(p4) + int(p5) + int(p6) + int(p7) + int(p8) + int(p9) + int(p10) + int(p11) + int(p12) + int(p13) + int(p14) + int(p15) + int(p16) + int(p17) + int(p18) + int(p19) + int(p20)
            rezz = Results.query.order_by(Results.res_sl_id.desc()).first() 
            rezz.lifestyle=resp
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
            r1 = request.form.get('q1')
            r2 = request.form.get('q2')
            r3 = request.form.get('q3')
            r4 = request.form.get('q4')
            r5 = request.form.get('q5')
            r6 = request.form.get('q6')
            r7 = request.form.get('q7')
            r8 = request.form.get('q8')
            r9 = request.form.get('q9')
            r10 = request.form.get('q10')
            r11 = request.form.get('q11')
            r12 = request.form.get('q12')
            r13 = request.form.get('q13')
            r14 = request.form.get('q14')
            r15 = request.form.get('q15')
            r16 = request.form.get('q16')


            resp = int(r1) + int(r2) + int(r3) + int(r4) + int(r5) + int(r6) + int(r7) + int(r8) + int(r9) + int(r10) + int(r11) + int(r12) + int(r13) + int(r14) + int(r15) + int(r16)
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
            s1 = request.form.get('q1')
            s2 = request.form.get('q2')
            s3 = request.form.get('q3')
            s4 = request.form.get('q4')
            s5 = request.form.get('q5')
            s6 = request.form.get('q6')
            s7 = request.form.get('q7')
            s8 = request.form.get('q8')
            s9 = request.form.get('q9')
            s10 = request.form.get('q10')
            s11 = request.form.get('q11')
            s12 = request.form.get('q12')
            s13 = request.form.get('q13')
            s14 = request.form.get('q14')
            s15 = request.form.get('q15')
            s16 = request.form.get('q16')

            resp = int(s1) + int(s2) + int(s3) + int(s4) + int(s5) + int(s6) + int(s7) + int(s8) + int(s9) + int(s10) + int(s11) + int(s12) + int(s13) + int(s14) + int(s15) + int(s16)
            rezz = Results.query.order_by(Results.res_sl_id.desc()).first() 
            rezz.symptoms=resp
            db.session.commit()
            return redirect(url_for('step2'))


@app.route('/result', methods=['GET','POST'])
def result():
    if session.get('loggedin') ==None:
        flash('Please sign in to take the various categories of Evaluation Tests','warning')
        return redirect('/') 
    else:
        id = session['loggedin']
        pfie = Results.query.order_by(Results.res_sl_id.desc()).first() 
        mdeets = Users.query.order_by(Users.user_id).all()
        userdeets = db.session.query(Users).get(id)
        total = pfie.employment + pfie.environment + pfie.lifestyle + pfie.personality + pfie.relationship + pfie.symptoms 
        if request.method=='GET':
            return render_template('users/result.html', pfie=pfie,mdeets=mdeets,total=total,id=id,userdeets=userdeets)


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
        total = pfie.sed_life_conval 
        if request.method=='GET':
            return render_template('users/result_social.html', pfie=pfie,mdeets=mdeets,total=total,id=id,userdeets=userdeets)

   

@app.route('/print_result1')
def print_result1():
    catname = db.session.query(Categories.cat_name).all()
    catpoint= db.session.query(Categories.cat_point).all()
    alldeets = db.session.query(Categories).all()
    deets = db.session.query(Categories.total_score).filter(Categories.cat_name=='total').one()
    mdeets = db.session.query(Categories.cat_id).all()

    return render_template('users/print_result1.html', deets=deets,mdeets=mdeets,catpoint=catpoint,catname=catname,alldeets=alldeets)


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
            slt1 = request.form.get('sl1')
            slt2 = request.form.get('sl2')
            slt3 = request.form.get('sl3')
            slt4 = request.form.get('sl4')
            slt5 = request.form.get('sl5')
            slt6 = request.form.get('sl6')
            slt7 = request.form.get('sl7')
            slt8 = request.form.get('sl8')
            slt9 = request.form.get('sl9')
            slt10 = request.form.get('sl10')
            slt11 = request.form.get('sl11')
            slt12 = request.form.get('sl12')
            slt13 = request.form.get('sl13')
            slt14 = request.form.get('sl14')
            slt15 = request.form.get('sl15')
            slt16 = request.form.get('sl16')
            slt17 = request.form.get('sl17')

            if slt1=='' or slt2=='' or slt3=='' or slt4=='' or slt5=='' or slt6=='' or slt7=='' or slt8=='' or slt9=='' or slt10=='' or slt11=='' or slt12=='' or slt13=='' or slt14=='' or slt15=='' or slt16=='' or slt17=='':
                flash('Kindly fill all the fields ','danger')
                return render_template('users/sedentary_lifestyle.html')
            else:
                resp = float(slt1) + float(slt2) + float(slt3) + float(slt4) + float(slt5) + float(slt6) + float(slt7) + float(slt8) + float(slt9) + float(slt10) + float(slt11) + float(slt12) + float(slt13) + float(slt14) + float(slt15) + float(slt16) + float(slt17)

                if resp >24:
                    flash('Kindly review your input for you cannot have more than 24 hours in a day','danger')
                    return render_template('users/sedentary_lifestyle.html')
                else:
                    conval = float(slt1)*0.8 + float(slt2)*0.8 + float(slt3)*1.5 + float(slt4)*1.5 + float(slt5)*1.5 + float(slt6)*1.5 + float(slt7)*1.5 + float(slt8)*2 + float(slt9)*3 + float(slt10)*4 + float(slt11)*5 + float(slt12)*3 + float(slt13)*4 + float(slt14)*5 + float(slt15)*7 + float(slt16)*8 + float(slt17)*9

                    rezz = Results.query.order_by(Results.res_sl_id.desc()).first() 
                    rezz.sed_life_hrs=resp
                    rezz.sed_life_conval=conval
                    
                    db.session.commit()
                    return redirect(url_for('result_sed'))


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
            soc1 = request.form.get('dos1')
            soc2 = request.form.get('dos2')
            soc3 = request.form.get('dos3')
            soc4 = request.form.get('dos4')
            soc5 = request.form.get('dos5')
            soc6 = request.form.get('dos6')
            soc7 = request.form.get('dos7')
            soc8 = request.form.get('dos8')
            soc9 = request.form.get('dos9')
            soc10 = request.form.get('dos10')
            soc11 = request.form.get('dos11')
            soc12 = request.form.get('dos12')
            soc13 = request.form.get('dos13')
            soc14 = request.form.get('dos14')
            soc15 = request.form.get('dos15')
            soc16 = request.form.get('dos16')
            soc17 = request.form.get('dos17')
            soc18 = request.form.get('dos18')
            soc19 = request.form.get('dos19')
            soc20 = request.form.get('dos20')
            soc21 = request.form.get('dos21')
            soc22 = request.form.get('dos22')
            soc23 = request.form.get('dos23')
            soc24 = request.form.get('dos24')
            soc25 = request.form.get('dos25')
            soc26 = request.form.get('dos26')
            soc27 = request.form.get('dos27')
            soc28 = request.form.get('dos28')
            soc29 = request.form.get('dos29')
            soc30 = request.form.get('dos30')
            soc31 = request.form.get('dos31')
            soc32 = request.form.get('dos32')
            soc33 = request.form.get('dos33')
            soc34 = request.form.get('dos34')
            soc35 = request.form.get('dos35')
            soc36 = request.form.get('dos36')
            soc37 = request.form.get('dos37')
            soc38 = request.form.get('dos38')
            soc39 = request.form.get('dos39')
            soc40 = request.form.get('dos40')
            soc41 = request.form.get('dos41')
            soc42 = request.form.get('dos42')
            soc43 = request.form.get('dos43')
            soc44 = request.form.get('dos44')

            resp = int(soc1) + int(soc2) + int(soc3) + int(soc4) + int(soc5) + int(soc6) + int(soc7) + int(soc8) + int(soc9) + int(soc10) + int(soc11) + int(soc12) + int(soc13) + int(soc14) + int(soc15) + int(soc16) + int(soc17) + int(soc18) + int(soc19) + int(soc20) + int(soc21) + int(soc22) + int(soc23) + int(soc24) + int(soc25) + int(soc26) + int(soc27) + int(soc28) + int(soc29) + int(soc30) + int(soc31) + int(soc32) + int(soc33) + int(soc34) + int(soc35) + int(soc36) + int(soc37) + int(soc38) + int(soc39) + int(soc40) + int(soc41) + int(soc42) + int(soc43) + int(soc44)
            rezz = Results.query.order_by(Results.res_sl_id.desc()).first() 
            rezz.social=resp
            db.session.commit()
            return redirect(url_for('result_social'))


@app.route('/bridals', methods=['GET','POST'])
def bridals():
    return render_template('users/bridals.html')
        
