from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired

class ProductForm(FlaskForm):
    mancode = StringField('Manufacturer Code', validators=[DataRequired()])
    usercode = StringField('User Code', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    category = SelectField('Category', choices=[('raw_material', 'Raw Material'), ('parts', 'Parts'), ('finished_product', 'Finished Product')], validators=[DataRequired()])
    location = SelectField('Location', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add Product')
