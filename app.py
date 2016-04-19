from flask import Flask, render_template, url_for, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField, SelectField, SubmitField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Required, Length, Email

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretico'
bootstrap = Bootstrap(app)


class LoginForm(Form):
    name = StringField('Introduce yourself', validators=[Required(), Length(1, 16)])
    password = PasswordField('Your Password', validators=[Required(), Length(1, 16)])
    submit = SubmitField('Submit')


class RegistrationForm(Form):
    name = StringField('What is your name?', validators=[Required(), Length(1, 16)])
    age = SelectField('Your age', choices=[(str(i), str(i)) for i in range(10, 100)])
    email = EmailField('Email address', validators=[Required(), Email()])
    password = PasswordField('Your Password', validators=[Required(), Length(1, 16)])
    submit = SubmitField('Register')

@app.route("/")
def welcome():
    return render_template("welcome.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    name = None
    password = None
    form = LoginForm()
    if form.validate_on_submit():
        name = form.name.data
        password = form.password.data
        form.name.data = ''
        form.password.data = ''
        return render_template("welcome.html")
    return render_template('login.html', form=form)


@app.route("/registration",methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    print form
    if form.validate_on_submit():
        name = form.name.data
        age = form.age.data
        email = form.email.data
        password = form.password.data
        form.name.data = ''
        form.age.data = ''
        form.email.data = ''
        form.password.data = ''
        return redirect(url_for('login'))
    return render_template("registration.html", form=form)

@app.route("/posts")
def posts():
    return render_template("posts.html")

if __name__ == "__main__":
    app.run(debug=True)