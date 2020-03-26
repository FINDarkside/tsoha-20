from application import app, db
from flask import redirect, render_template, request, url_for
from application.features.models import Feature
from application.features.forms import FeatureForm

@app.route("/features/", methods=["GET"])
def features_index():
    return render_template("features/list.html", features = Feature.query.all())

@app.route("/features/new/", methods=["GET"])
def features_form():
    return render_template("features/new.html", form = FeatureForm())

@app.route("/features/<feature_id>/edit", methods=["GET"])
def feature_requests_form(feature_id):
    feature = Feature.query.get(feature_id)
    return render_template("features/edit.html", feature = feature)

@app.route("/features/<feature_id>/edit", methods=["POST"])
def features_edit(feature_id):
    f = Feature.query.get(feature_id)
    f.title = request.form.get("title")
    f.description = request.form.get("description")
    db.session().commit()
    return redirect(url_for("features_index"))

@app.route("/features/", methods=["POST"])
def features_create():
    form = FeatureForm(request.form)
    feature = Feature(form.title.data,
                       form.description.data,
                       None)

    db.session().add(feature)
    db.session().commit()

    return redirect(url_for("features_index"))
