from application import app, db
from flask import redirect, render_template, request, url_for
from application.tasks.models import FeatureRequest

@app.route("/feature_requests/", methods=["GET"])
def feature_requests_index():
    return render_template("feature_requests/list.html", feature_requests = FeatureRequest.query.all())


@app.route("/feature_requests/new/")
def feature_requests_form():
    return render_template("feature_requests/new.html")


@app.route("/feature_requests/", methods=["POST"])
def feature_requests_create():
    t = FeatureRequest(request.form.get("title"),
                       request.form.get("description"),
                       None)

    db.session().add(t)
    db.session().commit()

    return redirect(url_for("feature_requests_index"))
