from database import db
from datetime import datetime
from sqlalchemy.orm import validates

class EnergyConsumption(db.Model):
    __tablename__="energy_consumption"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    amount = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())

    user = db.relationship("User", back_populates="energy_consumption")

    @validates("amount")
    def validate_amount(self, value):
        if not isinstance(value, float):
            raise ValueError("Amount must be a float")
        return value

    @validates("timestamp")
    def validate_timestamp(self, value):
        if value > datetime.now():
            raise ValueError("Timestamp cannot be in the future")
        return value

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'amount': self.amount,
            'time_stamp': self.timestamp
        }

    def __repr__(self):
        return f"<EnergyConsumption {self.id}>"