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

            new_forecast = Forecast(
                source=request.form['source'],
                forecast_amount=request.form['forecast_amount']
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
        
