# app/views.py

from flask import Blueprint, render_template, request, redirect, url_for, current_app

from app.forms import ProductForm
from .models import db, Location, Product, Stock
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def index():
    print(current_app)  # Tulostaa Flask-sovelluksen olion
    print(current_app.jinja_env.loader.list_templates())  # Tulostaa kaikki ladatut templaatit
    products = Product.query.all()
    return render_template('index.html', products=products)

@main.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        # Haetaan lomakkeelta tiedot
        mancode = request.form['mancode']
        usercode = request.form['usercode']
        description = request.form['description']
        category = request.form['category']
        location_id = request.form['location']

        # Luodaan uusi tuote tietokantaan
        new_product = Product(mancode=mancode, usercode=usercode, description=description, category=category, location_id=location_id)
        db.session.add(new_product)
        db.session.commit()

        return redirect(url_for('main.add_product'))

    locations = Location.query.all()
    return render_template('add_product.html', locations=locations, form=ProductForm())

@main.route('/stock/<int:product_id>', methods=['GET', 'POST'])
def stock(product_id):
    if request.method == 'POST':
        # Haetaan lomakkeelta tiedot
        quantity = int(request.form['quantity'])
        action = request.form['action']

        # Luodaan uusi varastotapahtuma tietokantaan
        new_stock = Stock(product_id=product_id, quantity=quantity, timestamp=datetime.now(), action=action)
        db.session.add(new_stock)
        db.session.commit()

    product = Product.query.get_or_404(product_id)
    stocks = Stock.query.filter_by(product_id=product_id).order_by(Stock.timestamp.desc()).all()
    return render_template('stock.html', product=product, stocks=stocks)

@main.route('/add_location', methods=['GET', 'POST'])
def add_location():
    locations = Location.query.all()  # Query all locations
    if request.method == 'POST':
        # Haetaan lomakkeelta tiedot
        type = request.form['type']
        shelf = request.form['shelf']
        # Käsittelylogiikka lomakkeen datalle ja tietokantaan tallennus

        # Luodaan uusi sijainti tietokantaan
        new_location = Location(type=type, shelf=shelf)
        db.session.add(new_location)
        db.session.commit()
        
        locations = Location.query.all()  # Query all locations
        return render_template('add_location.html', form=ProductForm(), locations=locations)
        
    # Jos HTTP-metodi on GET, renderöi lomakesivu
    return render_template('add_location.html', form=ProductForm(), locations=locations)

@main.route('/add_stock', methods=['GET', 'POST'])
def add_stock():
    if request.method == 'POST':
        # Käsittelylogiikka lomakkeen datalle ja tietokantaan tallennus
        return redirect(url_for('main.index'))  # Ohjaa takaisin pääsivulle

    # Jos HTTP-metodi on GET, renderöi lomakesivu
    return render_template('add_stock.html', form=ProductForm())

@main.route('/transfer_product', methods=['GET', 'POST'])
def transfer_product():
    if request.method == 'POST':
        # Käsittelylogiikka lomakkeen datalle ja tietokantaan tallennus
        return redirect(url_for('main.index'))  # Ohjaa takaisin pääsivulle

    # Jos HTTP-metodi on GET, renderöi lomakesivu
    return render_template('transfer_product.html', form=ProductForm())

@main.route('/remove_material', methods=['GET', 'POST'])
def remove_material():
    if request.method == 'POST':
        # Käsittelylogiikka lomakkeen datalle ja tietokantaan tallennus
        return redirect(url_for('main.index'))  # Ohjaa takaisin pääsivulle

    # Jos HTTP-metodi on GET, renderöi lomakesivu
    return render_template('remove_material.html', form=ProductForm())
