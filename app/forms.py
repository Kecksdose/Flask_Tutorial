from flask_wtf import Form
from wtforms import StringField, BooleanField, PasswordField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, Email

class UsernameMailPasswordRegisterForm(Form):
    nickname = StringField('Nickname', validators=[DataRequired(),
        Length(min=3, max=20)])
    email = StringField('E-Mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),
        Length(min=8, max=50)])

class UsernamePasswordLoginForm(Form):
    nickname = StringField('Nickname', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

class EditForm(Form):
    nickname = StringField('nickname', validators=[DataRequired()])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])
