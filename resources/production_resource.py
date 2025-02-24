from datetime import datetime
from flask import jsonify, request, make_response
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError
from database import db
from models.production_data import EnergyProduction

class ProductionResource(Resource):

    def get(self):
        try:
            productions = EnergyProduction.query.all()
            return jsonify([production.to_dict() for production in productions])
        except SQLAlchemyError as e:
            print(f"An error occurred: {e}")
            return {"message": "Internal server error"}, 500

    def post(self):
        try:
            timestamp_str = request.form.get('timestamp')
            timestamp = datetime.fromisoformat(timestamp_str) if timestamp_str else datetime.now()

            new_production = EnergyProduction(
                user_id=request.form['user_id'],
                source=request.form['source'],
                amount=request.form['amount'],
                timestamp=timestamp
            )
            db.session.add(new_production)
            db.session.commit()
            response_dict = new_production.to_dict()
            return make_response(jsonify(response_dict), 201)
        except KeyError as ke:
            print(f"Missing: {ke}")
            return make_response(jsonify({"error": f"Missing required field: {ke}"}), 400)

class ProductionByID(Resource):

    def get(self, energy_production_id):
        production = EnergyProduction.query.filter_by(id=energy_production_id).first()
        if production:
            return make_response(production.to_dict(), 200)
        return make_response(jsonify({"error": "Production not found"}), 404)

    def patch(self, energy_production_id):
        record = EnergyProduction.query.filter_by(id=energy_production_id).first()
        if not record:
            return make_response(jsonify({"error": "Production not found"}), 404)
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
                    return make_response(jsonify({"error": "Unable to update energy production", "details": str(e)}), 500)

    def delete(self, energy_production_id):
        record = EnergyProduction.query.filter_by(id=energy_production_id).first()
        if not record:
            return make_response(jsonify({"error": "Production not found"}), 404)
        try:
            db.session.delete(record)
            db.session.commit()
            return make_response({"message": "Production successfully deleted"}, 200)
        except SQLAlchemyError as e:
            db.session.rollback()
            return make_response(jsonify({"error": "Unable to delete production", "details": str(e)}), 500)