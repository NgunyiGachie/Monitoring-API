import pytest
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from app import app
from database import db
from models.forecast import Forecast

@pytest.fixture(scope='function', autouse=True)
def setup_database():
    """Fixture to set up and clean up the database before each test."""
    with app.app_context():
        db.create_all()
        yield
        db.session.rollback()
        db.session.close()

class TestForecast:
    """Test case for the Forecast model"""

    def test_has_attributes(self):
        """Test that the Forecast model has the required attributes"""
        with app.app_context():
            Forecast.query.delete()
            db.session.commit()

            forecast = Forecast(
                source = 'wind',
                forecast_amount = 20.5,
                timestamp = datetime(2025, 1, 1)
            )
            db.session.add(forecast)
            db.session.commit()

            created_forecast = Forecast.query.filter(Forecast.source == 'wind').first()
            assert created_forecast.source == 'wind'
            assert created_forecast.forecast_amount == 20.5
            assert created_forecast.timestamp == datetime(2025, 1, 1)

    def test_has_source(self):
        """Test that source is required"""
        with app.app_context():
            Forecast.query.delete()
            db.session.commit()

            forecast = Forecast(
                forecast_amount = 20.5,
                timestamp = datetime(2025, 1, 1)
            )
            with pytest.raises(IntegrityError):
                db.session.add(forecast)
                db.session.commit()

    def test_has_forecast_amount(self):
        """Test that a forecast amount is required"""
        with app.app_context():
            Forecast.query.delete()
            db.session.commit()

            forecast = Forecast(
                source = 'wind',
                timestamp = datetime(2025, 1, 1)
            )
            with pytest.raises(IntegrityError):
                db.session.add(forecast)
                db.session.commit()

    def test_has_timestamp(self):
        """Test that a timestamp is required"""
        with app.app_context():
            Forecast.query.delete()
            db.session.commit()

            forecast = Forecast(
                source = 'wind',
                forecast_amount = 20.5,
            )
            with pytest.raises(IntegrityError):
                db.session.add(forecast)
                db.session.commit()