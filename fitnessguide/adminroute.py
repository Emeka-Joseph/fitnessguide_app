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


@app.route('/admin_dashboard')
def admin_dashboard():
    allusers = db.session.query(Users).all()
    allresults = db.session.query(Results).all()
    return render_template('admin/admin_dashboard.html',allusers=allusers,allresults=allresults)