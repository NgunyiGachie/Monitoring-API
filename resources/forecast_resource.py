from datetime import datetime
from flask import jsonify, request, make_response
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError
from database import db
from models.forecast import Forecast

class ForecastResource(Resource):

    def get(self):
        try:
            forecasts = Forecast.query.all()
            return jsonify([forecast.to_dict() for forecast in forecasts])
        except SQLAlchemyError as e:
            print(f"An error occurred:{e}")
            return {"message": "Internal server error"}, 500

    def post(self):
        try:
            timestamp_str = request.form.get('timestamp')
            timestamp = datetime.fromisoformat(timestamp_str) if timestamp_str else datetime.now()
            source = request.form.get['source']
            forecast_amount_str = request.form.get['forecast_amount']
            try:
                forecast_amount = float(forecast_amount_str)
            except (TypeError, ValueError):
                return make_response(jsonify({"error": "Invalid amount format"}))

            new_forecast = Forecast(
                source=source,
                forecast_amount=forecast_amount,
                timestamp=timestamp
            )
            db.session.add(new_forecast)
            db.session.commit()
            response_dict = new_forecast.to_dict()
            return make_response(jsonify(response_dict), 201)
        except KeyError as ke:
            print(f"Missing: {ke}")
            return make_response(jsonify(response_dict), 201)
        except SQLAlchemyError as e:
            print (f"Error creating forecast: {e}")
            return make_response(jsonify({"error": "Unable to create forecast", "details": str(e)}, 500))

class ForecastByID(Resource):

    def get(self, forecast_id):
        forecast = Forecast.query.filter_by(id=forecast_id).first()
        if forecast:
            return make_response(forecast.to_dict(), 200)
        return make_response(jsonify({"error": "Forecast not found"}), 404)

    def patch(self, forecast_id):
        record = Forecast.query.filter_by(id=forecast_id).first()
        if not record:
            return make_response(jsonify({"error": "Forecast not found"}), 404)

        data = request.get_json()
        if not data:
            return make_response(jsonify({"error": "Invalid data format"}), 404)
        for attr, value in data.items():
            if attr == 'timestamp' and value:
                try:
                    value = datetime.fromisoformat(value)
                except ValueError:
                    return make_response(jsonify({"error": "Invalid date format"}), 400)
                if hasattr(record, attr):
                    setattr(record, attr, value)
            try:
                db.session.add(record)
                db.session.commit()
                return make_response(jsonify(record.to_dict()), 200)
            except SQLAlchemyError as e:
                db.session.rollback()
                return make_response(jsonify({"error": "Unable to update consumption", "details": str(e)}), 500)

    def delete(self, forecast_id):
        record = Forecast.query.filter_by(id=forecast_id).first()
        if not record:
            return make_response(jsonify({"error": "Forecast not found"}), 404)
        try:
            db.session.delete(record)
            db.session.commit()
            return make_response({"message": "Forecast successful deleted"}, 200)
        except SQLAlchemyError as e:
            db.session.rollback()
            return make_response(jsonify({"error": "Unable to delete forecast", "details": str(e)}), 500)