from flask_wtf import FlaskForm #用來初始化表單
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User

#TODO from app.models import User (DB)

class LoginForm(FlaskForm): #登入表單
    username = StringField('使用者名稱', validators=[DataRequired()])
    password = PasswordField('密碼', validators=[DataRequired()])
    remember_me = BooleanField('記住我')
    submit = SubmitField('登入')
    
class RegistrationForm(FlaskForm): #註冊表單
    username = StringField('使用者名稱', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('密碼', validators=[DataRequired()])
    password2 = PasswordField('再輸入一次密碼', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('註冊')

    def validate_username(self, username):  #WTF的自訂義validator(魔術方法magic methods)
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Pls use a different username.')
        
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email is not None:
            raise ValidationError('Pls use a different email address.')