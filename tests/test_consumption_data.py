import pytest
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from app import app
from database import db
from models.consumption_data import EnergyConsumption

@pytest.fixture(scope='function', autouse=True)
def setup_database():
    """Fixture to set up and clean up the database before each test."""
    with app.app_context():
        db.create_all()
        yield
        db.session.rollback()
        db.session.close()

class TestConsumption:
    """Test case for the Consumption model"""

    def test_has_attributes(self):
        """Test that the EnergyConsumption model has the required attributes"""
        with app.app_context():
            EnergyConsumption.query.delete()
            db.session.commit()

            energy_consumption = EnergyConsumption(
                user_id = 1,
                amount = 20.5,
                timestamp = datetime(2025, 1, 1)
            )
            db.session.add(energy_consumption)
            db.session.commit()

            created_energy_consumption = EnergyConsumption.query.filter(EnergyConsumption.amount == 20.5 ).first()
            assert created_energy_consumption.user_id == 1
            assert created_energy_consumption.amount == 20.5
            assert created_energy_consumption.timestamp == datetime(2025, 1,1)

    def test_requires_user_id(self):
        """Test that a user_id is required"""
        with app.app_context():
            EnergyConsumption.query.delete()
            db.session.commit()

            energy_consumption = EnergyConsumption(
                amount = 20.5,
                timestamp = datetime(2025, 1, 1)
            )
            with pytest.raises(IntegrityError):
                db.session.add(energy_consumption)
                db.session.commit()

    def test_requires_amount(self):
        """Test that amount is required"""
        with app.app_context():
            EnergyConsumption.query.delete()
            db.session.commit()

            energy_consumption = EnergyConsumption(
                user_id = 1,
                timestamp = datetime(2025, 1, 1)
            )
            with pytest.raises(IntegrityError):
                db.session.add(energy_consumption)
                db.session.commit()

    def test_requires_timestamp(self):
        """Test that timestamp is required"""
        with app.app_context():
            EnergyConsumption.query.delete()
            db.session.commit()

            energy_consumption = EnergyConsumption(
                user_id = 1,
                amount = 20.4,
            )
            with pytest.raises(IntegrityError):
                db.session.add(energy_consumption)
                db.session.commit()
