# app/views.py

from flask import Blueprint, render_template, request, redirect, url_for, current_app, flash

from app.forms import Form
from .models import db, Location, Product, Stock, Log
from datetime import datetime
#from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import or_

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
        new_location_id = int(request.form['to_location'])  # Convert to integer
        stock_to_update.location_id = new_location_id
        stock_to_update.quantity = int(request.form['quantity'])  # Convert to integer
        try:
            with db.session.no_autoflush:
                db.session.query(Stock).filter(Stock.id == id).update({
                    'quantity': stock_to_update.quantity,
                    'location_id': new_location_id
                })
            db.session.commit()
            flash('Stock updated successfully.')
            return redirect(url_for('main.transfer_product', id=id))
        except Exception as e:
            db.session.rollback()
            flash('Error: Stock update failed.')
            print(e)  # Print the exception for debugging purposes
            return render_template('transfer_product.html', form=form, stock_to_update=stock_to_update)
    else:
        return render_template('transfer_product.html', form=form, stock_to_update=stock_to_update)

# route to delete stock
@main.route('/delete_stock/<int:id>', methods=['GET', 'POST'])
def delete_stock(id):
    stock_to_delete = Stock.query.get(id)
    db.session.delete(stock_to_delete)
    db.session.commit()
    return redirect(url_for('main.add_stock'))

# route to delete product
@main.route('/delete_product/<int:id>', methods=['GET', 'POST'])
def delete_product(id):
    product_to_delete = Product.query.get(id)
    db.session.delete(product_to_delete)
    db.session.commit()
    return redirect(url_for('main.add_product'))

@main.route('/delete_location/<int:id>', methods=['GET', 'POST'])
def delete_location(id):
    location_to_delete = Location.query.get(id)
    db.session.delete(location_to_delete)
    db.session.commit()
    return redirect(url_for('main.add_location'))

@main.route('/logs')
def logs():
    logs = Log.query.all()
    return render_template('logs.html', logs=logs)

@main.route('/search_stock')
def search_stock():
    q = request.args.get('q')
    print(q)

    if q:
        stocks = Stock.query.join(Product).filter(
            or_(
                Product.description.icontains(q),
                Product.mancode.icontains(q),
                Product.usercode.icontains(q)
            )
        ).order_by(Product.description.asc(), Stock.timestamp.asc()).all()
    else:
        stocks = []
    return render_template('search_stock.html', stocks=stocks)

@main.route('/search_products')
def search_products():
    q = request.args.get('q')
    print(q)

    if q:
        products = Product.query.filter(
            or_(
                Product.description.icontains(q),
                Product.mancode.icontains(q),
                Product.usercode.icontains(q)
            )
        ).order_by(Product.description.asc()).all()
    else:
        products = []
    return render_template('search_products.html', products=products)

@main.route('/search_locations')
def search_locations():
    q = request.args.get('q')
    print(q)

    if q:
        locations = Location.query.filter(
            or_(
                Location.shelf.icontains(q),
                Location.type.icontains(q)
            )
        ).order_by(Location.shelf.asc()).all()
    else:
        locations = []
    return render_template('search_locations.html', locations=locations)