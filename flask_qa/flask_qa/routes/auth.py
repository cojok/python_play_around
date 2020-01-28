from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import check_password_hash
from flask_login import (login_user, logout_user)

from flask_qa.extensions import db
from flask_qa.models import User

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
       name = request.form['name']
       plain_password = request.form['password']
       
       user = User(
           name=name, 
           plain_password=plain_password,
           admin=False,
           expert=False
        )
       db.session.add(user)
       db.session.commit()
       
       return redirect(url_for('auth.login')) 
    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        error_message = ''
        
        user = User.query.filter_by(name=name).first()
        
        if not user or not check_password_hash(user.password, password):
            error_message = 'Username and/or password are wrong. Please try again!'
            
        if not error_message:
            login_user(user)
            return redirect(url_for('main.index'))
                
        
    return render_template('login.html')

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))