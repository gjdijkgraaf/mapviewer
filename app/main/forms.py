from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, RadioField, SubmitField, \
    TextAreaField, SelectField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

class AddProjectForm(FlaskForm):
    name = StringField('Project name', validators=[DataRequired()])
    description = StringField('Description')
    users = SelectMultipleField('Users', coerce=int)
    layers = SelectMultipleField('Layers', coerce=int)
    submit = SubmitField('Submit')

class EditProjectForm(FlaskForm):
    name = StringField('Project name', validators=[DataRequired()])
    description = StringField('Description')
    submit = SubmitField('Submit')

class LayerForm(FlaskForm):
    tablename = SelectField('Table name')
    description = StringField('Description')
    geometry_type = RadioField('Geometry type', choices=[('Point', 'Point'), ('Polyline', 'Polyline'), ('Polygon', 'Polygon')])
    geometry_column = StringField('Geometry column')
    id_column = StringField('ID column')
    submit = SubmitField('Submit')

class AddLayerviewForm(FlaskForm):
    project = SelectField('Project')
    layer = SelectField('Layer')
    name = StringField('Layerview name', validators=[DataRequired()])
    order = IntegerField('Order')
    description = StringField('Description')
    pointtolayer = TextAreaField('pointToLayer function')
    style = TextAreaField('style function')
    oneachfeature = TextAreaField('onEachFeature function')
    submit = SubmitField('Submit')

class LayerviewForm(FlaskForm):
    name = StringField('Layerview name', validators=[DataRequired()])
    order = IntegerField('Order')
    description = StringField('Description')
    pointtolayer = TextAreaField('pointToLayer function')
    style = TextAreaField('style function')
    oneachfeature = TextAreaField('onEachFeature function')
    submit = SubmitField('Submit')

class AddUser2ProjectForm(FlaskForm):
    users = SelectMultipleField('Users', coerce=int)
    submit = SubmitField('Submit')

class DeleteConfirmationForm(FlaskForm):
    confirmation = RadioField('Do you want to proceed?', choices=[('Yes', 'Yes'), ('No', 'No')])
    submit = SubmitField('Submit')
