from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

# Get the base directory of your project
basedir = os.path.abspath(os.path.dirname(__file__))

def create_app():
    app = Flask(__name__, template_folder='../templates')
   
   # Nämä kaksi riviä poistetaan kommenteista, kun käytät oikeaa sovellusta
    #secret_key = os.environ.get('SECRET_KEY')
    #app.config['SECRET_KEY'] = secret_key
    
    # Tämä on vain esimerkki, älä käytä tätä oikeassa sovelluksessa
    secret_key = 'fWwo52UukrUTj6YDNjPT' 
    app.config['SECRET_KEY'] = secret_key
    
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, '..', 'instance', 'varastonhallinta.db')

    db.init_app(app)  # Siirretään db.init_app(app) tähän kohtaan

    from app.views import main
    app.register_blueprint(main)

    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html'), 404

    return app
