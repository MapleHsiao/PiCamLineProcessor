import os
basedir = os.path.abspath(os.path.dirname(__file__))    #將當下執行的東西的相對路徑=>絕對路徑

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this-is-a-secret'
# secret_key = os.environ.get('SECRET_KEY')
# if secret_key:
#     print('OK')
# else:
#     print('not set')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False