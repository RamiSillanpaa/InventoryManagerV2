# app/views.py

from flask import Blueprint, render_template, request, redirect, url_for, current_app, flash

from app.forms import Form
from .models import db, Location, Product, Log
from datetime import datetime
from sqlalchemy import or_

main = Blueprint('main', __name__)

@main.route('/')
def index():
    print(current_app)
    print(current_app.jinja_env.loader.list_templates())
    locations = Location.query.filter(Location.quantity > 0).all()
    return render_template('index.html', locations=locations)

@main.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        mancode = request.form['mancode']
        usercode = request.form['usercode']
        description = request.form['description']
        category = request.form['category']
        reorder_point = request.form.get('reorder_point', 0)

        new_product = Product(mancode=mancode, usercode=usercode, description=description, 
                             category=category, reorder_point=reorder_point)
        db.session.add(new_product)
        db.session.commit()

        return redirect(url_for('main.add_product'))

    products = Product.query.all()
    return render_template('add_product.html', form=Form(), products=products)

@main.route('/add_location', methods=['GET', 'POST'])
def add_location():
    if request.method == 'POST':
        shelf = request.form['shelf']
        product_id = request.form.get('search_product')
        quantity = request.form.get('quantity', 0)
        
        new_location = Location(shelf=shelf, product_id=product_id, quantity=quantity)
        db.session.add(new_location)
        db.session.commit()
        
        # Log the addition
        timestamp = datetime.now()
        new_log = Log(event_type='CREATE', quantity_changed=quantity, 
                     product_id=product_id, location_id=new_location.id, timestamp=timestamp)
        db.session.add(new_log)
        db.session.commit()
        
        return redirect(url_for('main.add_location'))
        
    locations = Location.query.all()
    return render_template('add_location.html', form=Form(), locations=locations) 

@main.route('/add_stock', methods=['GET', 'POST'])
def add_stock():
    if request.method == 'POST':
        product_id = request.form['search_product']
        location_id = request.form['to_location']
        quantity = int(request.form['quantity'])
        timestamp = datetime.now()
        
        # Update Location quantity
        location = Location.query.get(location_id)
        location.quantity += quantity
        db.session.commit()
        
        # add to Log
        new_log = Log(event_type='UPDATE', quantity_changed=quantity, 
                     product_id=product_id, location_id=location_id, timestamp=timestamp)
        db.session.add(new_log)
        db.session.commit()
        
        return redirect(url_for('main.add_stock'))

    # Get locations with inventory
    locations = Location.query.filter(Location.quantity > 0).all()
    return render_template('add_stock.html', form=Form(), locations=locations)

@main.route('/transfer_product/<int:id>', methods=['GET', 'POST'])
def transfer_product(id):
    form = Form()
    location_to_update = Location.query.get(id)
    
    if request.method == 'POST':
        new_quantity = int(request.form['quantity'])
        quantity_change = new_quantity - location_to_update.quantity
        location_to_update.quantity = new_quantity
        
        try:
            db.session.commit()
            
            # Log the transfer
            new_log = Log(event_type='UPDATE', quantity_changed=quantity_change,
                         product_id=location_to_update.product_id, location_id=id)
            db.session.add(new_log)
            db.session.commit()
            
            flash('Inventory updated successfully.')
            return redirect(url_for('main.transfer_product', id=id))
        except Exception as e:
            db.session.rollback()
            flash('Error: Inventory update failed.')
            print(e)
            return render_template('transfer_product.html', form=form, location_to_update=location_to_update)
    else:
        return render_template('transfer_product.html', form=form, location_to_update=location_to_update)

# route to delete stock
@main.route('/delete_location/<int:id>', methods=['GET', 'POST'])
def delete_location(id):
    location_to_delete = Location.query.get(id)
    
    # Log the deletion
    new_log = Log(event_type='DELETE', quantity_changed=-location_to_delete.quantity,
                 product_id=location_to_delete.product_id, location_id=id)
    db.session.add(new_log)
    
    db.session.delete(location_to_delete)
    db.session.commit()
    return redirect(url_for('main.add_location'))

# route to delete product
@main.route('/delete_product/<int:id>', methods=['GET', 'POST'])
def delete_product(id):
    product_to_delete = Product.query.get(id)
    
    # First log deletions for all locations containing this product
    locations = Location.query.filter_by(product_id=id).all()
    for location in locations:
        new_log = Log(event_type='DELETE', quantity_changed=-location.quantity,
                     product_id=id, location_id=location.id)
        db.session.add(new_log)
    
    db.session.delete(product_to_delete)
    db.session.commit()
    return redirect(url_for('main.add_product'))

@main.route('/logs')
def logs():
    logs = Log.query.all()
    return render_template('logs.html', logs=logs)

@main.route('/search_stock')
def search_stock():
    q = request.args.get('q')
    print(q)

    if q:
        locations = Location.query.join(Product).filter(
            or_(
                Product.description.icontains(q),
                Product.mancode.icontains(q),
                Product.usercode.icontains(q)
            )
        ).order_by(Product.description.asc()).all()
    else:
        locations = []
    return render_template('search_stock.html', locations=locations)

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
                Location.shelf.icontains(q)
            )
        ).order_by(Location.shelf.asc()).all()
    else:
        locations = []
    return render_template('search_locations.html', locations=locations)