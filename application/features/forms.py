from flask_wtf import FlaskForm
from wtforms import StringField, validators
from wtforms.widgets import TextArea

class FeatureForm(FlaskForm):
    title = StringField("Title", [validators.Length(min=4)])
    description = StringField("Description", widget=TextArea())
 
    class Meta:
        csrf = False

