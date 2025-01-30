import pytest
from sqlalchemy.exc import IntegrityError
from argon2 import PasswordHasher
from database import db
from models.user import User