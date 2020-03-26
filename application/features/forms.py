from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.widgets import TextArea

class FeatureForm(FlaskForm):
    title = StringField("Title")
    description = StringField("Description", widget=TextArea())
 
    class Meta:
        csrf = False

