from flask import Flask, render_template, url_for, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField, SelectField, SubmitField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Required, Length, Email
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretico'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)


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


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), index=True, unique=True)
    age = db.Column(db.Integer)
    email = db.Column(db.String(16), unique=True)
    password = db.Column(db.String(16))

    def __repr__(self):
        return '<User {0}>'.format(self.name)

@app.route("/")
def welcome():
    return render_template("welcome.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    name = None
    password = None
    form = LoginForm()
    new = False
    if form.validate_on_submit():
        name = form.name.data
        password = form.password.data
        form.name.data = ''
        form.password.data = ''
        if User.query.filter_by(name=name).first() is None:
            new = True
            return render_template('login.html', form=form, new=new)
        return render_template("welcome.html", name=name)
    return render_template('login.html', form=form)


@app.route("/registration",methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        name = form.name.data
        age = form.age.data
        email = form.email.data
        password = form.password.data
        form.name.data = ''
        form.age.data = ''
        form.email.data = ''
        form.password.data = ''
        if User.query.filter_by(name=name).first() is None:
            db.session.add(User(name=name, age=age, email=email, password=password))
            db.session.commit()
        return redirect(url_for('login'))
    return render_template("registration.html", form=form)

@app.route("/posts")
def posts():
    return render_template("posts.html")

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)