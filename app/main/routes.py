from flask import render_template, redirect, url_for
from flask_login import login_required, login_user, logout_user
from ..models import User
from . import main
from .forms import LoginForm, RegistrationForm


@main.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        password = form.password.data
        user = User.query.filter_by(name=form.name.data).first()
        if user is not None and user.verify_password(password):
            login_user(user, form.remember_me.data)
            return redirect(url_for('main.welcome'))
        elif user is None:
            new = True
            return render_template('login.html', form=form, new=new)
        else:
            wrong_pass = True
            return render_template('login.html', form=form, name=user.name, wrong_pass=wrong_pass)
    return render_template('login.html', form=form)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.welcome'))


@main.route("/")
def welcome():
    return render_template("welcome.html")


@main.route("/registration", methods=['GET', 'POST'])
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
            User.register(name, age, email, password)
        else:
            already_exists = True
            return render_template("registration.html", form=form, already_exists=already_exists, name=name)
        return redirect(url_for('main.login'))
    return render_template("registration.html", form=form)


@main.route("/disk")
def disk():
    return render_template("disk.html")