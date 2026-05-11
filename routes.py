# routes.py
from flask import Blueprint, jsonify, request
from models import db, Bill

api_bp = Blueprint('api', __name__)

# --- Dummy Auth Routes to stop the frontend from redirecting to Login ---
@api_bp.route('/me', methods=['GET'])
def current_user():
    # Fake user data to bypass login during testing
    return jsonify({"user": {"username": "TestUser", "email": "test@example.com"}}), 200

@api_bp.route('/login', methods=['POST'])
def login():
    return jsonify({"user": {"username": "TestUser", "email": "test@example.com"}}), 200

# --- Bill Management Routes ---
@api_bp.route('/bills', methods=['GET'])
def get_bills():
    bills = Bill.query.all()
    # Use the clean to_dict method from our model
    return jsonify([bill.to_dict() for bill in bills]), 200

@api_bp.route('/bills', methods=['POST'])
def add_bill():
    data = request.get_json()
    new_bill = Bill(
        name=data.get('name'),
        amount=float(data.get('amount')),
        currency=data.get('currency', 'USD'),
        due_date=data.get('due_date'),
        category=data.get('category'),
        frequency=data.get('frequency', 'once')
    )
    db.session.add(new_bill)
    db.session.commit()
    return jsonify(new_bill.to_dict()), 201

@api_bp.route('/bills/<int:bill_id>', methods=['DELETE'])
def delete_bill(bill_id):
    bill = Bill.query.get(bill_id)
    if bill:
        db.session.delete(bill)
        db.session.commit()
        return jsonify({"message": "Bill deleted"}), 200
    return jsonify({"error": "Not found"}), 404

@api_bp.route('/bills/<int:bill_id>/pay', methods=['PATCH'])
def pay_bill(bill_id):
    bill = Bill.query.get(bill_id)
    if bill:
        bill.status = 'paid'
        db.session.commit()
        return jsonify(bill.to_dict()), 200
    return jsonify({"error": "Not found"}), 404