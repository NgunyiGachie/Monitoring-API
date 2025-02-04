from database import db
from datetime import datetime
from sqlalchemy.orm import validates

class Forecast(db.Model):
    __tablename__ ="forecasts"

    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String, nullable=False)
    forecast_amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    @validates("source")
    def validate_source(self, value):
        if not isinstance(value, str):
            raise ValueError("Source must be a string")
        return value

    @validates("forecast_amount")
    def validate_forecast_amount(self, value):
        if not isinstance(value, float):
            raise ValueError("Forecast amount must be a float")
        return value

    @validates("timestamp")
    def validate_timestamp(self, value):
        if value > datetime.utcnow():
            raise ValueError("Datetime cannot be in the future")
        return value

    def to_dict(self):
        return {
            "id": self.id,
            "source": self.source,
            "forecast_amount": self.forecast_amount,
            "timestamp": self.timestamp,
        }

    def __repr__(self):
        return f"<Forecast {self.id}>"