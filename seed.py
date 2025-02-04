import os
from database import db
from models.consumption_data import EnergyConsumption
from models.forecast import Forecast
from models.production_data import EnergyProduction
from models.user import User
from app import app
from config import config
from argon2 import PasswordHasher
from datetime import datetime

ph = PasswordHasher()
config_name = os.getenv('FLASK_CONFIG', 'default')
app.config.from_object(config[config_name])

with app.app_context():
    print("Dropping all tables....")
    db.drop_all()
    print("Creating all tables....")
    db.create_all()

    users = [
        
    ]