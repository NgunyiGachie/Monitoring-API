from database import db
from datetime import datetime
from sqlalchemy.orm import validates

class EnergyConsumption(db.Model):
    __tablename__="energy_consumptions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    user = db.relationship("User", back_populates="energy_consumption")

    @validates("amount")
    def validate_amount(self, key, value):
        if not isinstance(value, float):
            raise ValueError("Amount must be a float")
        return value

    @validates("timestamp")
    def validate_timestamp(self, key, value):
        if value > datetime.now():
            raise ValueError("Timestamp cannot be in the future")
        return value

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'amount': self.amount,
            'timestamp': self.timestamp
        }

    def __repr__(self):
        return f"<EnergyConsumption {self.id}>"