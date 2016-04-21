from flask import Flask, render_template, url_for, redirect, request
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField, SelectField, SubmitField, PasswordField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Required, Length, Email
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretico'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
lm = LoginManager(app)
lm.login_view = 'login'


class LoginForm(Form):
    name = StringField('Introduce yourself', validators=[Required(), Length(1, 16)])
    password = PasswordField('Your Password', validators=[Required(), Length(1, 16)])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Submit')


class RegistrationForm(Form):
    name = StringField('What is your name?', validators=[Required(), Length(1, 16)])
    age = SelectField('Your age', choices=[(str(i), str(i)) for i in range(10, 100)])
    email = EmailField('Email address', validators=[Required(), Email()])
    password = PasswordField('Your Password', validators=[Required(), Length(1, 16)])
    submit = SubmitField('Register')


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), index=True, unique=True)
    age = db.Column(db.Integer)
    email = db.Column(db.String(16), unique=True)
    password_hash = db.Column(db.String(64))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def register(name, age, email, password):
        user = User(name=name, age=age, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    def __repr__(self):
        return '<User {0}>'.format(self.name)

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

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
        password = form.password.data
        user = User.query.filter_by(name=form.name.data).first()
        if user is not None and user.verify_password(password):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('welcome'))
        elif user is None:
            new = True
            return render_template('login.html', form=form, new=new)
        else:
            wrong_pass = True
            return render_template('login.html', form=form, name=user.name, wrong_pass=wrong_pass)
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('welcome'))


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
            user = User.register(name, age, email, password)
            db.session.add(user)
            db.session.commit()
        else:
            already_exists = True
            return render_template("registration.html", form=form, already_exists=already_exists, name=name)
        return redirect(url_for('login'))
    return render_template("registration.html", form=form)

@app.route("/posts")
def posts():
    return render_template("posts.html")

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)