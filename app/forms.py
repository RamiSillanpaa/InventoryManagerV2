# app/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, IntegerField, SearchField
from wtforms.validators import DataRequired
from wtforms_sqlalchemy.fields import QuerySelectField
from app.models import Location, Product, Stock

def get_locations():
    # Function to retrieve locations from the database
    # Replace this with your actual implementation
    return Location.query.all()

def get_products():
    # Function to retrieve products from the database
    # Replace this with your actual implementation
    return Product.query.all()

def get_products_in_stock():
    # Function to retrieve products from the database
    # Replace this with your actual implementation
    return Product.query.join(Stock, Product.id == Stock.product_id).all()

class Form(FlaskForm):
    # new product
    mancode = StringField('Manufacturer Code', validators=[DataRequired()])
    usercode = StringField('User Code', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    category = SelectField('Category', choices=[('raw_material', 'Raw Material'), ('parts', 'Parts'), ('finished_product', 'Finished Product')], validators=[DataRequired()])
    # new location
    create_location = StringField('Location', validators=[DataRequired()])
    type = SelectField('Type', choices=[('outside', 'Outside'), ('inside', 'Inside'), ('yard', 'Yard')], validators=[DataRequired()])
    shelf = StringField('Shelf', validators=[DataRequired()])
    # add stock
    search_product = QuerySelectField('Product', query_factory=get_products, get_label='description', validators=[DataRequired()])
    to_location = QuerySelectField('To location', query_factory=get_locations, get_label='shelf', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    # transfer product
    product_in_stock = StringField('Product', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    # submit button
    submit = SubmitField('Submit')
