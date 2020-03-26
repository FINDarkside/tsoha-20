from application import app
from flask import render_template, request, redirect, url_for
from application.auth.models import User
from application.auth.forms import LoginForm


@app.route("/auth/login", methods=["GET"])
def auth_login_form():
    return render_template("auth/login.html", form=LoginForm())


@app.route("/auth/login", methods=["POST"])
def auth_login():
    form = LoginForm(request.form)
    # mahdolliset validoinnit

    user = User.query.filter_by(
        username=form.username.data, password=form.password.data).first()

    if not user:
        return render_template("auth/login.html", form=form, error="No such username or password")

    print(user.username + " logged in")
    return redirect(url_for("index"))
