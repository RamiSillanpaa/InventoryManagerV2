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

@main.route('/transfer_product/<int:id>', methods=['GET', 'POST'])
def transfer_product(id):
    form = Form()
    stock_to_update = Stock.query.get(id)
    if request.method == 'POST':
        stock_to_update.location = request.form['location']
        stock_to_update.quantity = request.form['quantity']
        try:
            db.session.commit()
            flash('Stock updated successfully.')
            return render_template('transfer_product.html', form=form, stock_to_update=stock_to_update)
        except:
            flash('Error: Stock update failed.')
            return render_template('transfer_product.html', form=form, stock_to_update=stock_to_update)
    else:
        return render_template('transfer_product.html', form=form, stock_to_update=stock_to_update)

@main.route('/remove_material', methods=['GET', 'POST'])
def remove_material():
    if request.method == 'POST':
        # Käsittelylogiikka lomakkeen datalle ja tietokantaan tallennus
        return redirect(url_for('main.remove_material'))  # Ohjaa takaisin pääsivulle

    # Jos HTTP-metodi on GET, renderöi lomakesivu
    return render_template('remove_material.html', form=Form())
