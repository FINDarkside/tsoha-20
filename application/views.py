from flask import render_template
from application import app
from application.auth.models import User


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/stats/")
def stats():
    top_users = User.find_users_with_most_features()
    return render_template("stats.html", users=top_users)
