from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_socketio import SocketIO

app = Flask(__name__, static_folder='../static')   #初始化Flask
app.config.from_object(Config)  #SECRET_KEY

db = SQLAlchemy(app)
migrate = Migrate(app, db)  #注意他要連結app和db

login = LoginManager(app)
login.login_view = 'login'
login.login_message = '你需要登錄才能訪問這個頁面。'

socketio = SocketIO(app)
from app import routes, models
