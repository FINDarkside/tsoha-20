from application import app, db
from flask import redirect, render_template, request, url_for
from application.features.models import Feature, Like
from application.features.forms import FeatureForm
from flask_login import login_required, current_user


@app.route("/features/", methods=["GET"])
def features_index():
    return render_template("features/list.html", features=Feature.query.all())


@app.route("/features/new/", methods=["GET"])
@login_required
def features_new_form():
    return render_template("features/new.html", form=FeatureForm())


@app.route("/features/<feature_id>/edit", methods=["GET"])
@login_required
def features_edit_form(feature_id):
    feature = Feature.query.get(feature_id)
    form = FeatureForm()
    form.title.data = feature.title
    form.description.data = feature.description
    return render_template("features/edit.html", form=form, feature_id=feature.id)


@app.route("/features/<feature_id>/edit", methods=["POST"])
@login_required
def features_edit(feature_id):
    form = FeatureForm(request.form)
    if not form.validate():
        return render_template("features/edit.html", form=form, feature_id=feature_id)
    feature = Feature.query.get(feature_id)

    feature.title = form.title.data
    feature.description = form.description.data
    db.session().commit()
    return redirect(url_for("features_index"))


@app.route("/features/", methods=["POST"])
@login_required
def features_create():
    form = FeatureForm(request.form)
    if not form.validate():
        return render_template("features/new.html", form=form)

    feature = Feature(form.title.data,
                      form.description.data,
                      current_user.id)

    db.session().add(feature)
    db.session().commit()

    return redirect(url_for("features_index"))


@app.route("/features/<feature_id>/delete", methods=["POST"])
@login_required
def features_delete(feature_id):
    feature = Feature.query.get(feature_id)
    db.session.delete(feature)
    db.session.commit()
    return redirect(url_for("features_index"))


@app.route("/features/<feature_id>/like", methods=["POST"])
@login_required
def features_like(feature_id):
    print(current_user.id)
    like = Like(feature_id, current_user.id)

    db.session().add(like)
    db.session().commit()
    return redirect(url_for("features_index"))
