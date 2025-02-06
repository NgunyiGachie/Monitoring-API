import os
from flask import Flask
from flask_migrate import Migrate
from config import config
from database import db
from models import User, EnergyConsumption, EnergyProduction, Forecast

app = Flask(__name__)

config_name = os.getenv("FLASK_CONFIG", "default")
app.config.from_object(config[config_name])

db.init_app(app)
migrate = Migrate(app, db)

if __name__ == '__main__':
    try:
        port = int(os.environ.get("PORT", 5555))
        app.run(host='0.0.0.0', port=port, debug=True)
    except (ValueError, RuntimeError) as e:
        print(f"An error occurred: {e}")
