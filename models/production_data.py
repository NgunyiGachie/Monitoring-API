from database import db
from sqlalchemy.orm import validates
from datetime import datetime

class EnergyProduction(db.Model):
    __tablename__="energy_production"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    source = db.Column(db.String, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", back_populates="energy_production")

    @validates('amount')
    def validate_amount(self, value):
        if not isinstance(value, float):
            raise ValueError("Amount must be a float")
        return value

    @validates("timestamp")
    def validate_timestamp(self, value):
        if value > datetime.utcnow():
            raise ValueError("Timestamp cannot be in the future")
        return value

    @validates('source')
    def validate_source(self, value):
        if not isinstance(value, str):
            raise ValueError("Source must be a string")
        return value

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'source': self.source,
            'amount': self.amount,
            'timestamp': self.timestamp,
        }

    def __repr__(self):
        return f"<EnergyProduction {self.id}>"
