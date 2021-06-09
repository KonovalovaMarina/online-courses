from flask_wtf import FlaskForm
from wtforms import (FieldList, StringField, SubmitField)


class Sample(FlaskForm):
    name = StringField()
    flist = FieldList(StringField())
    submit = SubmitField('Submit')
