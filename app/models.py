# app/models.py

from app import db

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #location/type of storage
    type = db.Column(db.String(20), nullable=False)
    #shelf identifier
    shelf = db.Column(db.String(20), nullable=False)
    products = db.relationship('Product', back_populates='location')

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #manufacturers product code
    mancode = db.Column(db.String(50), nullable=False)
    #user's own product code
    usercode = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    #default location for product
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    location = db.relationship('Location', back_populates='products')
    stocks = db.relationship('Stock', back_populates='product')

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product = db.relationship('Product', back_populates='stocks')
    quantity = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    action = db.Column(db.String(20), nullable=False)
