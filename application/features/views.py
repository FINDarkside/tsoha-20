from application import app, db
from flask import redirect, render_template, request, url_for
from application.features.models import Feature

@app.route("/features/", methods=["GET"])
def features_index():
    return render_template("features/list.html", features = Feature.query.all())


@app.route("/features/new/")
def features_form():
    return render_template("features/new.html")

@app.route("/features/", methods=["POST"])
def features_create():
    f = Feature(request.form.get("title"),
                       request.form.get("description"),
                       None)

    db.session().add(f)
    db.session().commit()

    return redirect(url_for("features_index"))
