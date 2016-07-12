from flask_wtf import Form
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Length

class UsernamePasswordForm(Form):
    nickname = StringField('Nickname', validators=[DataRequired(),
        Length(min=3, max=20)])
    password = PasswordField('Password', validators=[DataRequired(),
        Length(min=8, max=50)])
    remember_me = BooleanField('remember_me', default=False)
