import os

class Config(object):
    config = os.environ.get('SECRET_KEY') or 'this-is-a-secret'
# secret_key = os.environ.get('SECRET_KEY')
# if secret_key:
#     print('OK')
# else:
#     print('not set')