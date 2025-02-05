import os
from datetime import timedelta
from cryptography.fernet import Fernet

def generate_key():
    return Fernet.generate_key().decode()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', generate_key())
    if SECRET_KEY == generate_key():
        print("Warning: Using a generated SECRET_KEY. Please set SECRET_KEY in the environment.")

    PROPAGATE_EXCEPTIONS = True
    API_TITLE = "Renewable Energy Monitoring API"
    API_VERSION = "V1"
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'energy.db')}")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your_jwt_secret_key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)

    def __repr__(self):
        return f"<Config {self.API_TITLE}, Version: {self.API_VERSION}>"

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True

    def __repr__(self):
        return "<DevelopmentConfig>"

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory'

    def __repr__(self):
        return f"<TestingConfig>"

class ProductionConfig(Config):
    DEBUG = False

    def __repr__(self):
        return f"<ProductionConfig>"

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}