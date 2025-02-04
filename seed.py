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
        User(
           username = 'antogachie',
           email = 'myemail@gmail.com',
           image_url = 'https://example.com/images/antogachie.jpg',
           created_at = datetime(2025, 2, 1)
        ),
        User(
            username = 'mrmorty',
            email = 'morty@gmail.com',
            image_url = 'https://example.com/images/morty.jpg',
            created_at = datetime(2025, 2, 1)
        )
    ]
    for user, password in zip(users, ['password1', 'password2']):
        user.password_hash = ph.hash(password)
    print("adding users to the database....")
    db.session.add_all(users)
    db.session.commit()
    print(f"{len(users)} users added")

    # Seed consumption
    consumption = [
        EnergyConsumption(
            user_id = 1,
            amount = 20.5,
            timestamp = datetime(2025, 1, 1),
        ),
        EnergyConsumption(
            user_id = 2,
            amount = 25.4,
            timestamp = datetime(2025, 1, 1)
        )
    ]
    try:
        print("Adding energy consumption to the database....")
        db.session.add_all(consumption)
        db.session.commit()
        print(f"{len(consumption)} consumption added")
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {e}")
    finally:
        db.session.close()