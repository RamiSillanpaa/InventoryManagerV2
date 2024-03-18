# app/views.py

from flask import Blueprint, render_template, request, redirect, url_for, current_app, flash

from app.forms import Form
from .models import db, Location, Product, Stock, Log
from datetime import datetime
#from sqlalchemy.orm.exc import NoResultFound

main = Blueprint('main', __name__)

@main.route('/')
def index():
    print(current_app)  # Tulostaa Flask-sovelluksen olion
    print(current_app.jinja_env.loader.list_templates())  # Tulostaa kaikki ladatut templaatit
    stocks = Stock.query.all()
    return render_template('index.html', stocks=stocks)

@main.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        # Haetaan lomakkeelta tiedot
        mancode = request.form['mancode']
        usercode = request.form['usercode']
        description = request.form['description']
        category = request.form['category']

        # Luodaan uusi tuote tietokantaan
        new_product = Product(mancode=mancode, usercode=usercode, description=description, category=category)
        db.session.add(new_product)
        db.session.commit()

        return redirect(url_for('main.add_product'))

    products = Product.query.all()
    return render_template('add_product.html', form=Form(), products=products)

@main.route('/add_location', methods=['GET', 'POST'])
def add_location():
    if request.method == 'POST':
        # Haetaan lomakkeelta tiedot
        type = request.form['type']
        shelf = request.form['shelf']
        # Käsittelylogiikka lomakkeen datalle ja tietokantaan tallennus
        # Luodaan uusi sijainti tietokantaan
        new_location = Location(type=type, shelf=shelf)
        db.session.add(new_location)
        db.session.commit()
        return redirect(url_for('main.add_location'))
        
    # Jos HTTP-metodi on GET, renderöi lomakesivu
    locations = Location.query.all()
    return render_template('add_location.html', form=Form(), locations=locations) 

@main.route('/add_stock', methods=['GET', 'POST'])
def add_stock():
    
    if request.method == 'POST':
        product_id = request.form['search_product']
        location_id = request.form['to_location']
        quantity = request.form['quantity']
        timestamp = datetime.now()
        product = Product.query.get(product_id)
        location = Location.query.get(location_id)
        
        # add to Stock
        input_stock = Stock(location=location, product=product, quantity=quantity, timestamp=timestamp)
        db.session.add(input_stock)
        db.session.commit()
        
        # add to Log
        new_log = Log(event_type='in', quantity_changed=quantity, to_location_id=location_id, product=product_id, timestamp=timestamp)
        db.session.add(new_log)
        db.session.commit()
        return redirect(url_for('main.add_stock'))

    # Jos HTTP-metodi on GET, renderöi lomakesivu
    stocks = Stock.query.all()
    return render_template('add_stock.html', form=Form(), stocks=stocks)

@main.route('/transfer_product', methods=['GET', 'POST'])
def transfer_product():
    if request.method == 'POST':
        product_id = request.form['product_in_stock']
        from_location = SelectField('From Location')

        def __init__(self, *args, **kwargs):
            product_id = kwargs.pop('product_id', None)
            super(Form, self).__init__(*args, **kwargs)
            if product_id:
                # Filter the locations based on the product_id
                self.from_location.choices = [(location.id, location.name) for location in Location.query.filter_by(product=product_id).all()]
            else:
                self.from_location.choices = []
        from_location = Stock.query.filter_by(product=product_id).all()
        product = Product.query.get(product_id)
        location = Location.query.get(from_location)
        current_quantity = Stock.quantity.query.filter_by(product=product, location=location).first()
        destination_location = request.form['destination_location']
        quantity = request.form['quantity']
        timestamp = datetime.now()
        # Check if quantity is a valid integer
        if not quantity.isdigit():
            flash('Error: Quantity must be a valid integer.')
            return redirect(url_for('main.transfer_product'))
        
        # Update database with the new location
        # If quantity is smaller than the stock, update the stock and create new stock for the destination location
        if int(quantity) < current_quantity:
            # update current quantity
            current_quantity -= int(quantity)
            new_stock = Stock(product=product, quantity=int(quantity), timestamp=timestamp, location=destination_location)
            db.session.add(new_stock)
            db.session.commit()
        # If quantity is equal to the stock, update the stock with the new location
        elif int(quantity) == current_quantity:
            from_location = destination_location
            db.session.commit()
        # If quantity is greater than the stock, return an error message
        else:
            flash('Error: Quantity is greater than the available stock.')
        return redirect(url_for('main.transfer_product'))

    # Jos HTTP-metodi on GET, renderöi lomakesivu
    return render_template('transfer_product.html', form=Form())

@main.route('/remove_material', methods=['GET', 'POST'])
def remove_material():
    if request.method == 'POST':
        # Käsittelylogiikka lomakkeen datalle ja tietokantaan tallennus
        return redirect(url_for('main.remove_material'))  # Ohjaa takaisin pääsivulle

    # Jos HTTP-metodi on GET, renderöi lomakesivu
    return render_template('remove_material.html', form=Form())
