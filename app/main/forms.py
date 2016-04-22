from flask_wtf import Form
from wtforms import StringField, SelectField, SubmitField, PasswordField, BooleanField
from wtforms.validators import Required, Length, Email, EqualTo
from wtforms.fields.html5 import EmailField

class LoginForm(Form):
    name = StringField('Introduce yourself', validators=[Required(), Length(1, 16)])
    password = PasswordField('Your Password', validators=[Required(), Length(1, 16)])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Submit')


class RegistrationForm(Form):
    name = StringField('What is your name?', validators=[Required(), Length(1, 16)])
    age = SelectField('Your age', choices=[(str(i), str(i)) for i in range(10, 100)])
    email = EmailField('Email address', validators=[Required(), Email()])
    password = PasswordField('Your Password', validators=[Required(), Length(1, 16),
                                                          EqualTo('pass_repeat', message='Passwords must match.')])
    pass_repeat = PasswordField('Repeat Password', validators=[Required(), Length(1, 16)])
    submit = SubmitField('Register')