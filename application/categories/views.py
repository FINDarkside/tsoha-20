from application import app, db
from flask import redirect, render_template, request, url_for
from application.categories.models import FeatureCategory
from application.features.forms import FeatureForm
from flask_login import login_required, current_user


@app.route("/categories/", methods=["GET"])
@login_required
def categories_edit_form():
    if not current_user.is_admin:
        return render_template("error.html", error="Unauthorized")
    categories = FeatureCategory.get_all()
    return render_template("categories/edit.html", categories=categories)


@app.route("/categories/<category_id>", methods=["POST"])
@login_required
def categories_edit(category_id):
    if not current_user.is_admin:
        return render_template("error.html", error="Unauthorized")

    category = FeatureCategory.query.get(category_id)
    if(not category):
        return render_template("error.html", error="Category not found")

    categories = FeatureCategory.get_all()

    new_name = request.form.get('name')
    if(not isinstance(new_name, str) or len(new_name) < 3):
        return render_template("categories/edit.html", categories=categories, error="Category name must be at least 3 characters long")
    if(len(new_name) > 20):
        return render_template("categories/edit.html", categories=categories, error="Category name must be less than 21 characters long")

    category.name = new_name
    db.session().commit()

    return render_template("categories/edit.html", categories=categories)


@app.route("/categories/new", methods=["POST"])
@login_required
def categories_create():
    if not current_user.is_admin:
        return render_template("error.html", error="Unauthorized")

    categories = FeatureCategory.get_all()

    name = request.form.get('name')
    if(not isinstance(name, str) or len(name) < 3):
        return render_template("categories/edit.html", categories=categories, error="Category name must be at least 3 characters long")
    if(len(name) > 20):
        return render_template("categories/edit.html", categories=categories, error="Category name must be less than 21 characters long")

    category = FeatureCategory(name)
    db.session().add(category)
    db.session().commit()
    
    return redirect(url_for("categories_edit_form"))
