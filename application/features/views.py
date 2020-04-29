from application import app, db
from flask import redirect, render_template, request, url_for
from application.features.models import Feature, Like
from application.categories.models import FeatureCategory
from application.features.forms import FeatureForm
from flask_login import login_required, current_user

features_per_page = 10

@app.route("/features/", methods=["GET"])
def features_index():
    categories = FeatureCategory.query.all()

    current_category = None
    if(request.args.get("category")):
        param_category_id = int(request.args.get("category"))
        for category in categories:
            if category.id == param_category_id:
                current_category = category
                break
    else:
        current_category = categories[0]

    if(current_category == None):
        return render_template("error.html", error="Invalid feature category")

    features = Feature.get_paginated(0, features_per_page, current_category.id)

    return render_template("features/list.html", features=features, categories=categories, current_category=current_category)


@app.route("/features/new/", methods=["GET"])
@login_required
def features_new_form():
    return render_template("features/new.html", form=FeatureForm())


@app.route("/features/<feature_id>/edit", methods=["GET"])
@login_required
def features_edit_form(feature_id):
    feature = Feature.query.get(feature_id)
    if(not feature.authorized_to_modify):
        return render_template("error.html", error="Unauthorized")
    form = FeatureForm()
    form.title.data = feature.title
    form.description.data = feature.description

    categories = FeatureCategory.get_all()
    return render_template("features/edit.html", form=form, feature=feature, categories=categories)


@app.route("/features/<feature_id>/edit", methods=["POST"])
@login_required
def features_edit(feature_id):
    form = FeatureForm(request.form)
    if not form.validate():
        return render_template("features/edit.html", form=form, feature_id=feature_id, categories=FeatureCategory.get_all())
    feature = Feature.query.get(feature_id)

    if not feature.authorized_to_modify:
        return render_template("error.html", error="Unauthorized")

    if current_user.is_admin and request.form.get('category'):
        category = FeatureCategory.query.get(request.form.get('category'))
        if not category:
            return render_template("error.html", error="Invalid category")
        feature.category_id = category.id

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
    if(not feature.authorized_to_modify):
        return render_template("error.html", error="Unauthorized")
    db.session.delete(feature)
    db.session.commit()
    return redirect(url_for("features_index"))


@app.route("/features/<feature_id>/like", methods=["POST"])
@login_required
def features_like(feature_id):
    feature = Feature.query.get(feature_id)
    if(not feature.current_user_liked):
        like = Like(feature_id, current_user.id)
        db.session().add(like)
        db.session().commit()
    return redirect(url_for("features_index"))


@app.route("/features/<feature_id>/unlike", methods=["POST"])
@login_required
def features_unlike(feature_id):
    feature = Feature.query.get(feature_id)
    if(feature.current_user_liked):
        like = db.session.query(Like).filter_by(
            user_id=current_user.id, feature_id=feature_id).first()
        db.session().delete(like)
        db.session().commit()
    return redirect(url_for("features_index"))
