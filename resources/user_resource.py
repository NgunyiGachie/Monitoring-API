from datetime import datetime
from flask import jsonify, request, make_response
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError
from database import db
from models.user import User

class UserResource(Resource):

    def get(self):
        try:
            users = User.query.all()
            return jsonify([user.to_dict() for user in users])
        except SQLAlchemyError as e:
            print(f"An error occurred: {e}")
            return {"message": "Internal server error"}, 500

    def post(self):
        try:
            created_at_str = request.form.get('created_at')
            created_at = datetime.fromisoformat(created_at_str) if created_at_str else datetime.now()

            password = request.form.get('password')

            new_user = User(
                username = request.form['username'],
                email = request.form['email'],
                image_url = request.form['image_url'],
                created_at = created_at
            )
            new_user.password = password

            db.session.add(new_user)
            db.session.commit()
            response_dict = new_user.to_dict()
            return make_response(jsonify(response_dict), 201)
        except KeyError as ke:
            print(f"Missing: {ke}")
            return make_response(jsonify({"error": f"Missing required field: {ke}"}), 400)
        except SQLAlchemyError as e:
            print(f"Error creating user: {e}")
            return make_response(jsonify({"error": "Unable to create user", "details": str(e)}), 500)

class UserByID(Resource):

    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if user:
            return make_response(user.to_dict(), 200)
        return make_response(jsonify({"error": "User not found"}), 404)

    def patch(self, user_id):
        record = User.query.filter_by(id=user_id).first()
        if not record:
            return make_response(jsonify({"error": "User not found"}), 404)
        data = request.get_json()
        if not data:
            return make_response(jsonify({"error": "Invalid data format"}), 404)
        for attr, value in data.items():
            if attr == 'created_at' and value:
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
            return make_response(jsonify({"error": "Unable to update user", "details": str(e)}), 500)

    def delete(self, user_id):
        record = User.query.filter_by(id=user_id).first()
        if not record:
            return make_response(jsonify({"error": "User not found"}), 404)
        try:
            db.session.delete(record)
            db.session.commit()
            return make_response({"message": "User successfully deleted"}, 200)
        except SQLAlchemyError as e:
            db.session.rollback()
            return make_response(jsonify({"error": "Unable to delete user", "details": str(e)}), 500)
