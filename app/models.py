# app/models.py

from app import db
from sqlalchemy import DateTime
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy.schema import FetchedValue


class Location(db.Model):
    # Shelf unique id
    # redundant?
    # id = db.Column(db.Integer, primary_key=True)
    
    # Shelf identifier, unique
    shelf = db.Column(db.String(20), nullable=False, unique=True)
    
    # Location type (inside, outside, yard)
    type = db.Column(db.String(20), nullable=False)
    
    # Products in this location
    quantity = db.Column(db.Integer, nullable=True, default=0)
    
    # Products in this location
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    
    # Logs from this location
    product = db.relationship('Product', back_populates='locations')
    stocks = db.relationship('Stock', back_populates='location')

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False, unique=True)
    category = db.Column(db.String(20), nullable=False)
    mancode = db.Column(db.String(50), nullable=True, unique=True)
    usercode = db.Column(db.String(50), nullable=True, unique=True)
    locations = db.relationship('Location', back_populates='product')
    stocks = db.relationship('Stock', back_populates='product')

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, server_default=func.now(), server_onupdate=FetchedValue())
    quantity = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    product = db.relationship('Product', back_populates='stocks')
    location = db.relationship('Location', back_populates='stocks')

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=func.now(), onupdate=False)
    event_type = db.Column(db.String(50), nullable=False)
    quantity_changed = db.Column(db.Integer, nullable=False)
    from_location_id = db.Column(db.Integer, nullable=True)
    to_location_id = db.Column(db.Integer, nullable=False)
    product = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Log('{self.event_type}', '{self.quantity_changed}', '{self.product}', '{self.timestamp}')"