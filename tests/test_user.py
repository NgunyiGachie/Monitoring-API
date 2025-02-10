import pytest
from sqlalchemy.exc import IntegrityError
from argon2 import PasswordHasher
from datetime import datetime
from app import app
from database import db
from models.user import User

ph = PasswordHasher()

@pytest.fixture(scope='function', autouse=True)
def setup_database():
    """Fixture to set up and clean up the database before each test."""
    with app.app_context():
        db.create_all()
        yield
        db.session.rollback()
        db.session.close()

class TestUser:
    """Test case for the User model"""

    def test_has_attributes(self):
        """Test that the User model has the required attributes"""
        with app.app_context():
            db.session.execute(db.delete(User))
            db.session.commit()

            user = User(
                username = 'antony',
                email = 'gachie@antony.com',
                image_url = 'https://example.com/images/antogachie.jpg',
                created_at = datetime(2025, 1, 1)
            )
            user.password_hash = ph.hash('thewerewolfmaniam')
            db.session.add(user)
            db.session.commit()

            created_user = User.query.filter(User.username == 'antony').first()
            assert created_user.username == 'antony'
            assert created_user.email == 'gachie@antony.com'
            assert created_user.image_url == 'https://example.com/images/antogachie.jpg'
            assert created_user.created_at == datetime(2025, 1, 1)
            assert created_user.authenticate('thewerewolfmaniam')

    def test_requires_username(self):
        """Test that a username is required"""
        with app.app_context():
            User.query.delete()
            db.session.commit()

            user = User(
                email = 'gachie@antony.com',
                image_url = 'https://example.com/images/antogachie.jpg',
                created_at = datetime(2025, 1, 1)
            )
            with pytest.raises(IntegrityError):
                db.session.add(user)
                db.session.commit()

    def test_requires_email(self):
        """Test that an email is required"""
        with app.app_context():
            User.query.delete()
            db.session.commit()

            user = User(
                username = 'antony',
                image_url = 'https://example.com/images/antogachie.jpg',
                created_at = datetime(2025, 1, 1)
            )
            with pytest.raises(IntegrityError):
                db.session.add(user)
                db.session.commit()

    def test_requires_image_url(self):
        """Test that an image_url is required"""
        with app.app_context():
            User.query.delete()
            db.session.commit()

            user = User(
                username = 'antony',
                email = 'gachie@antony.com',
                created_at = datetime(2025, 1, 1)
            )
            with pytest.raises(IntegrityError):
                db.session.add(user)
                db.session.commit()
