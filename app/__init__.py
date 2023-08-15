from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)   #初始化Flask
app.config.from_object(Config)  #SECRET_KEY

db = SQLAlchemy(app)
migrate = Migrate(app, db)  #注意他要連結app和db

login = LoginManager(app)
login.login_view = 'login'
from app import routes, models
