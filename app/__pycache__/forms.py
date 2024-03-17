# app/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, IntegerField, SearchField
from wtforms.validators import DataRequired
from wtforms_sqlalchemy.fields import QuerySelectField
from app.models import Location, Product

def get_locations():
    # Function to retrieve locations from the database
    # Replace this with your actual implementation
    return Location.query.all()

def get_products():
    # Function to retrieve products from the database
    # Replace this with your actual implementation
    return Product.query.all()

class ProductForm(FlaskForm):
    # Manufacturers product code
    mancode = StringField('Manufacturer Code', validators=[DataRequired()])
    # User's own product code
    usercode = StringField('User Code', validators=[DataRequired()])
    # Product description / name
    description = StringField('Description', validators=[DataRequired()])
    # Product category (raw material, parts, finished product)
    category = SelectField('Category', choices=[('raw_material', 'Raw Material'), ('parts', 'Parts'), ('finished_product', 'Finished Product')], validators=[DataRequired()])
    # Product location
    location = QuerySelectField('Location', query_factory=get_locations, get_label='shelf', validators=[DataRequired()])
    #location/type of storage (outside, inside, yard)
    type = SelectField('Type', choices=[('outside', 'Outside'), ('inside', 'Inside'), ('yard', 'Yard')], validators=[DataRequired()])
    #shelf identifier
    shelf = StringField('Shelf', validators=[DataRequired()])
    product = StringField('Product', validators=[DataRequired()])
    destination_location = SelectField('Destination Location', coerce=int, validators=[DataRequired()])
    source_location = SelectField('Source Location', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add Product')

class StockForm(FlaskForm):
    # Quantity of stock
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    # Stock action (in, out)
    # action = SelectField('Action', choices=[('in', 'In'), ('out', 'Out')], validators=[DataRequired()])
    submit = SubmitField('Add Stock')
    product = QuerySelectField('Product', query_factory=get_products, get_label='description', validators=[DataRequired()])
    location = QuerySelectField('Location', query_factory=get_locations, get_label='shelf', validators=[DataRequired()])

class MoveForm(FlaskForm):
    #stock = QuerySelectField('Stock', query_factory=, get_label='id', validators=[DataRequired()])
    product = QuerySelectField('Product', query_factory=get_products, get_label='description', validators=[DataRequired()])
    source_location = QuerySelectField('Source Location', query_factory=get_locations, get_label='shelf', validators=[DataRequired()])
    destination_location = QuerySelectField('Destination Location', query_factory=get_locations, get_label='shelf', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Update Stock')