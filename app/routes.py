from app import app, db, socketio
from flask import render_template, url_for, flash, redirect, request, jsonify, session
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse
from app.AppUtility import CapturePicture, ProcessPicture
from app.AppUtility import toline, format_analysis_results

@app.route('/')
@app.route('/index')
@login_required
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
            flash('錯誤的帳戶名稱或密碼')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)    #執行登入(這邊flask_login的技術很多)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logut')
@login_required
def logout():
    logout_user()   #直接使用flask_login的function
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:   #這屬於Usermix提供的語法
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():   
        #記得判斷是從user按下submit開始所以使用這個function
        #vlidate_on_submit這邊會執行我們自訂義的validator
        user = User(username=form.username.data, email=form.email.data) 
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('恭喜，你現在是已經註冊的用戶!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/capture', methods=['GET', 'POST'])
@socketio.on('capture_image')
@login_required
def picture():
    if request.method == 'POST':
        try:
            result = CapturePicture()

            if result["status"] != "success":
                return jsonify({"capture": result})
            
            analysis_results = ProcessPicture()
            if analysis_results.get('status') == 'error':
                if "Face could not be detected" in analysis_results.get('message'):
                    analysis_results['message'] = "無檢測到臉部"

                return jsonify({"capture": result, "analysis": analysis_results})

            # 儲存數據session
            session['analysis_results'] = analysis_results

            combined_results = {
                'capture': result,
                'analysis': analysis_results
            }
            return jsonify(combined_results)
        except Exception as e:
            # 可以記錄 e 的詳細資訊，例如寫入到日誌文件
            return jsonify({"capture": {"status": "error", "message": str(e)}})
    else:
        return render_template('deepface.html', title='DeepFace')
    
# --------------------service--------------------
@app.route('/service/deepface/toline', methods=['POST'])
# @login_required
def line():
    analysis_results = session.get('analysis_results', None)    #從session讀取數據

    if not analysis_results:
        return jsonify({"status": "error", "message": "session中並無儲存資訊，請先在上一步進行分析"})

    try:
        msg = format_analysis_results(analysis_results)
        response=toline(msg)

        if response.status_code == 200:
            session.pop('analysis_results', None)
            return jsonify({"status": "success"})
        else:
            return jsonify({"status": "error", "message": response.text})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})