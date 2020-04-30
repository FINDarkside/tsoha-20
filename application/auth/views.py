from application import app, db, bcrypt
from flask import render_template, request, redirect, url_for
from application.auth.models import User
from application.auth.forms import LoginForm, RegisterForm
from flask_login import login_user, logout_user, login_required


@app.route("/auth/login", methods=["GET"])
def auth_login_form():
    return render_template("auth/login.html", form=LoginForm())


@app.route("/auth/login", methods=["POST"])
def auth_login():
    form = LoginForm(request.form)
    if not form.validate():
        return render_template("auth/login.html", form=form)

    user = User.query.filter_by(username=form.username.data).first()
    if(not user):
        return render_template("auth/login.html", form=form, error="No such username or password")
    if not bcrypt.check_password_hash(user.password, form.password.data):
        return render_template("auth/login.html", form=form, error="No such username or password")

    print(user.username + " logged in")
    login_user(user)

    return redirect(url_for("features_index"))


@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("features_index"))


@app.route("/auth/register", methods=["GET"])
def auth_register_form():
    return render_template("auth/register.html", form=RegisterForm())


@app.route("/auth/register", methods=["POST"])
def auth_register():
    form = RegisterForm(request.form)
    if not form.validate():
        return render_template("auth/register.html", form=form)
    print(form.password.data)
    password_hash = bcrypt.generate_password_hash(
        form.password.data).decode("utf-8")
    user = User(form.username.data, password_hash)
    db.session().add(user)
    db.session().commit()
    login_user(user)
    print(user.username + " created and logged in")
    return redirect(url_for("features_index"))
