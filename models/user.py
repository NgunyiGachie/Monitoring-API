"""
Tracks user information and preferences for carbon offset calculations
"""
from ..database import db
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError
from sqlalchemy.orm import validates

ph = PasswordHasher

class User(db.Model):
    __tablename__= "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False)
    _password_hash = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    ##Relationships (to be written)
    energy_consumption = db.relationship('energy_onsumption', back_populates='users', cascade='all, delete-orphan')

    @property
    def password_hash(self):
        raise AttributeError("Password hashes cannot be viewed")

    @password_hash.setter
    def password_hash(self, password):
        self._password_hash = ph.hash(password)

    def authenticate(self, password):
        try:
            ph.verify(self._password_hash, password)
            return True
        except VerificationError:
            return False

    @validates("username")
    def validate_username(self, username):
        if not username:
            raise AssertionError("No username provided")
        if User.query.filter(User.username == username).first():
            raise AssertionError("Usernae is already in use")
        if len(username) < 5 or len(username) > 20:
            raise AssertionError("Username must be between 5 and 20 characters")
        return username

    @validates("email")
    def validate_email(self, email):
        if not email:
            raise AssertionError("No email provided")
        if User.query.filter(User.email == email).first():
            raise AssertionError("Email is already in use")
        if '@' not in email:
            raise AssertionError("Invalid email")
        return email

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'image_url': self.image_url,
            'created_at': self.created_at,
        }

    def __repr__(self):
        return f"<User {self.username}, ID: {self.id}>"
