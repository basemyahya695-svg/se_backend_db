from flask import Blueprint, jsonify
from database import db
from models import Bill
from config import (
    BILL_STATUS_UNPAID, BILL_STATUS_PAID, EXCHANGE_RATES,
    VALID_CURRENCIES, VALID_BILL_CATEGORIES
)
from utils import (
    get_request_data, get_current_user_id, login_required,
    error_response, success_response, parse_date, format_date,
    validate_required_fields, validate_frequency, convert_currency
)

bills_bp = Blueprint('bills', __name__)

def find_user_bill_or_404(bill_id):
    return Bill.query.filter_by(id=bill_id, user_id=get_current_user_id()).first()

def serialize_bill(bill):
    return {
        "id": bill.id,
        "name": bill.name,
        "category": bill.category,
        "amount": bill.amount,
        "currency": bill.currency,
        "due_date": format_date(bill.due_date),
        "frequency": bill.frequency,
        "status": bill.status,
    }

@bills_bp.route("/api/bills", methods=["GET"])
@login_required
def get_bills():
    bills = Bill.query.filter_by(
        user_id=get_current_user_id()
    ).order_by(Bill.due_date.asc()).all()
    return jsonify([serialize_bill(bill) for bill in bills]), 200

@bills_bp.route("/api/bills", methods=["POST"])
@login_required
def add_bill():
    data = get_request_data()
    required_error = validate_required_fields(data, ["name", "amount", "due_date", "frequency"])
    if required_error:
        return error_response(required_error, 400)
    frequency_error = validate_frequency(data["frequency"])
    if frequency_error:
        return error_response(frequency_error, 400)
    currency = str(data.get("currency", "USD")).upper()
    if currency not in VALID_CURRENCIES:
        return error_response(f"Invalid currency. Use one of: {', '.join(sorted(VALID_CURRENCIES))}", 400)
    category = str(data.get("category", "other")).lower()
    if category not in VALID_BILL_CATEGORIES:
        return error_response(f"Invalid bill type. Use one of: {', '.join(sorted(VALID_BILL_CATEGORIES))}", 400)
    try:
        new_bill = Bill(
            user_id=get_current_user_id(),
            name=data["name"],
            category=category,
            amount=float(data["amount"]),
            currency=currency,
            due_date=parse_date(data["due_date"]),
            frequency=data["frequency"],
            status=BILL_STATUS_UNPAID,
        )
        db.session.add(new_bill)
        db.session.commit()
        return success_response("Bill added successfully", 201)
    except ValueError as error:
        return error_response(str(error), 400)

@bills_bp.route("/api/bills/<int:bill_id>", methods=["PUT"])
@login_required
def update_bill(bill_id):
    bill = find_user_bill_or_404(bill_id)
    if not bill:
        return error_response("Bill not found", 404)
    data = get_request_data()
    try:
        if "name" in data:
            bill.name = data["name"]
        if "category" in data:
            category = str(data["category"]).lower()
            if category not in VALID_BILL_CATEGORIES:
                return error_response(f"Invalid bill type. Use one of: {', '.join(sorted(VALID_BILL_CATEGORIES))}", 400)
            bill.category = category
        if "amount" in data:
            bill.amount = float(data["amount"])
        if "currency" in data:
            currency = str(data["currency"]).upper()
            if currency not in VALID_CURRENCIES:
                return error_response(f"Invalid currency. Use one of: {', '.join(sorted(VALID_CURRENCIES))}", 400)
            bill.currency = currency
        if "due_date" in data:
            bill.due_date = parse_date(data["due_date"])
        if "frequency" in data:
            freq_error = validate_frequency(data["frequency"])
            if freq_error:
                return error_response(freq_error, 400)
            bill.frequency = data["frequency"]
        db.session.commit()
        return success_response("Bill updated successfully")
    except ValueError as error:
        return error_response(str(error), 400)

@bills_bp.route("/api/bills/<int:bill_id>", methods=["DELETE"])
@login_required
def delete_bill(bill_id):
    bill = find_user_bill_or_404(bill_id)
    if not bill:
        return error_response("Bill not found", 404)
    db.session.delete(bill)
    db.session.commit()
    return success_response("Bill deleted successfully")

@bills_bp.route("/api/bills/<int:bill_id>/pay", methods=["PATCH"])
@login_required
def mark_bill_as_paid(bill_id):
    bill = find_user_bill_or_404(bill_id)
    if not bill:
        return error_response("Bill not found", 404)
    bill.status = BILL_STATUS_PAID
    db.session.commit()
    return success_response("Bill marked as paid")

@bills_bp.route("/api/bills/<int:bill_id>/convert/<string:currency>", methods=["GET"])
@login_required
def get_converted_bill(bill_id, currency):
    bill = find_user_bill_or_404(bill_id)
    if not bill:
        return error_response("Bill not found", 404)

    converted_amount = convert_currency(bill.amount, currency)
    
    if converted_amount is None:
        valid_list = ", ".join(EXCHANGE_RATES.keys())
        return error_response(f"Unsupported currency. Use one of: {valid_list}", 400)

    return jsonify({
        "id": bill.id,
        "name": bill.name,
        "original_amount_usd": bill.amount,
        "converted_amount": converted_amount,
        "currency": currency.upper()
    }), 200
