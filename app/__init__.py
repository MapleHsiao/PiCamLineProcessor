from flask import Flask
from config import Config

app = Flask(__name__)   #初始化Flask
app.config.from_object(Config)  #SECRET_KEY

from app import routes
#, models