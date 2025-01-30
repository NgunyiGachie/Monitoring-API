import os
from flask import Flask
from database import db

app = Flask(__name__)

config_name = os.getenv("FLASK_CONFIG", "default")
app.config.from_object(config[config_name])

db.init_app(app)
