# app/models.py

from app import db
from sqlalchemy import DateTime
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy.schema import FetchedValue

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    mancode = db.Column(db.String(50), nullable=True, unique=True)
    usercode = db.Column(db.String(50), nullable=True, unique=True)
    reorder_point = db.Column(db.Integer, nullable=False, default=0)
    
    locations = db.relationship('Location', back_populates='product')
    logs = db.relationship('Log', back_populates='product')

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shelf = db.Column(db.String(100), nullable=False, unique=True)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    product = db.relationship('Product', back_populates='locations')
    logs = db.relationship('Log', back_populates='location')

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=func.now())
    event_type = db.Column(db.String(50), nullable=False)  # CREATE, READ, UPDATE, DELETE
    quantity_changed = db.Column(db.Integer, nullable=True)
    
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    product = db.relationship('Product', back_populates='logs')
    
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    location = db.relationship('Location', back_populates='logs')
    
    def __repr__(self):
        return f"Log('{self.event_type}', '{self.quantity_changed}', '{self.product.description}', '{self.timestamp}')"