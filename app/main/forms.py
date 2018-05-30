from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, RadioField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

class AddProjectForm(FlaskForm):
    name = StringField('Project name', validators=[DataRequired()])
    description = StringField('Description')
    users = SelectMultipleField('Users', coerce=int)
    layers = SelectMultipleField('Layers', coerce=int)
    submit = SubmitField('Submit')

class LayerForm(FlaskForm):
    tablename = StringField('Table name', validators=[DataRequired()])
    description = StringField('Description')
    type = RadioField('Layer type', choices=[('Point', 'Point'), ('Polyline', 'Polyline'), ('Polygon', 'Polygon')])
    submit = SubmitField('Submit')
