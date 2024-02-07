from flask import render_template, request, redirect, url_for
from . import app, db
from .models import Location, Product, Stock
from datetime import datetime

@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/add_product', methods=['GET', 'POST'])
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

        return redirect(url_for('index'))

    locations = Location.query.all()
    return render_template('add_product.html', locations=locations)

@app.route('/stock/<int:product_id>', methods=['GET', 'POST'])
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
