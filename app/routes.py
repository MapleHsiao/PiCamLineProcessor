from app import app, db
from flask import render_template, url_for, flash, redirect, request
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
def index():
    title = 'Home'
    return render_template('index.html', title=title)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:   #先判斷是否已經登入
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data): #用User class定義的方法來確認密碼
            flash('Invalid Username Or Password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)    #執行登入(這邊flask_login的技術很多)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)