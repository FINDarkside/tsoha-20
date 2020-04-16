from flask_wtf import FlaskForm
from wtforms import StringField, validators
from wtforms.widgets import TextArea


class FeatureForm(FlaskForm):
    title = StringField("Title", [validators.Length(min=4, max=255)])
    description = StringField(
        "Description", [validators.Length(min=0, max=2000)], widget=TextArea())

    class Meta:
        csrf = False
