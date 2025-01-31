import pytest
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from app import app
from database import db
from models.production_data import EnergyProduction

class TestProduction:
    """Test case for the EnergyProduction model"""

    def test_has_attributes(self):
        """Test that the EnergyProduction model has the required attributes"""
        with app.app_context():
            EnergyProduction.query.delete()
            db.session.commit()

            energy_production = EnergyProduction(
                user_id = 1,
                source = 'wind',
                amount = 15,
                timestamp = datetime(2025, 1, 1)
            )
            db.session.add(energy_production)
            db.session.commit()

            created_energy_production = EnergyProduction.query.filter(EnergyProduction.user_id == 1).first()
            assert created_energy_production.user_id == 1
            assert created_energy_production.source == 'wind'
            assert created_energy_production.amount == 15
            assert created_energy_production.timestamp == datetime(2025, 1, 1)

    def test_has_user_id(self):
        """Test that a user_id is required"""
        with app.app_context():
            EnergyProduction.query.delete()
            db.session.commit()

            energy_production = EnergyProduction(
                source = 'wind',
                amount = 15,
                timestamp = datetime(2025, 1, 1)
            )
            with pytest.raises(IntegrityError):
                db.session.add(energy_production)
                db.session.commit()

    def test_has_source(self):
        """Test that source is required"""
        with app.app_context():
            EnergyProduction.query.delete()
            db.session.commit()

            energy_production = EnergyProduction(
                user_id = 1,
                amount = 15,
                timestamp = datetime(2025, 1, 1)
            )
            with pytest.raises(IntegrityError):
                db.session.add(energy_production)
                db.session.commit()

    def test_has_amount(self):
        """Test that amount is required"""
        with app.app_context():
            EnergyProduction.query.delete()
            db.session.commit()

            energy_production = EnergyProduction(
                user_id = 1,
                source = 'wind',
                timestamp = datetime(2025, 1, 1)
            )
            with pytest.raises(IntegrityError):
                db.session.add(energy_production)
                db.session.commit()

    def test_has_timestamp(user):
        """Test that timestamp is required"""
        with app.app_context():
            EnergyProduction.query.delete()
            db.session.commit()

            energy_production = EnergyProduction(
                user_id = 1,
                source = 'wind',
                amount = 15,
            )
            with pytest.raises(IntegrityError):
                db.session.add(energy_production)
                db.session.commit()