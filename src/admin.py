import os 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin
from models import db, Planets, Characters, Vehicles, Favorites, User

app = Flask(__name__)

def setup_admin(app):
    DATABASE_URL = os.getenv('DATABASE_URL', "postgres://", "postgresql://")
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'any key works')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    

    db =SQLAlchemy(app)
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    admin.add_view(ModelView(Planets, db.session))
    admin.add_view(ModelView(Characters, db.session))
    admin.add_view(ModelView(Vehicles, db.session))
    admin.add_view(ModelView(Favorites, db.session))
    admin.add_view(ModelView(User, db.session))
