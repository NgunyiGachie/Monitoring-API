from datetime import datetime
from flask import jsonify, request, make_response
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError
from database import db
from models.consumption_data import EnergyConsumption

class ConsumptionResource(Resource):

    def get(self):
        try:
            consumptions = EnergyConsumption.query.all()
            return jsonify([consumption.to_dict() for consumption in consumptions])
        except SQLAlchemyError as e:
            print(f"An error occurred: {e}")
            return {"message": "Internal server error"}, 500

    def post(self):
        try:
            timestamp_str = request.form.get('timestamp')
            timestamp = datetime.fromisoformat(timestamp_str) if timestamp_str else datetime.now()

            new_consumption = EnergyConsumption(
                user_id=request.form['user_id'],
                amount=request.form['amount'],
                timestamp=timestamp
            )
            db.session.add(new_consumption)
            db.session.commit()
            response_dict = new_consumption.to_dict()
            return make_response(jsonify(response_dict), 201)
        except KeyError as ke:
            print(f"Missing: {ke}")
            return make_response(jsonify({"error": f"Missing required field: {ke}"}), 400)
        except SQLAlchemyError as e:
            print(f"Error creating energy consumption: {e}")
            return make_response(jsonify({"error": "Unable to create energy consumption", "details": str(e)}, 500))

class ConsumptionByID(Resource):

    def get(self, energy_consumption_id):
        consumption = EnergyConsumption.query.filter_by(id=energy_consumption_id).first()
        if consumption:
            return make_response(consumption.to_dict(), 200)
        return make_response(jsonify({"error": "Consumption not found"}), 404)

    def patch(self, energy_consumption_id):
        record = EnergyConsumption.query.filter_by(id=energy_consumption_id).first()
        if not record:
            return make_response(jsonify({"error": "consumption not found"}), 404)
        data = request.get_json()
        if not data:
            return make_response(jsonify())
