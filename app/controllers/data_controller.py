from http import HTTPStatus
from typing import Tuple, Union

from flask import Blueprint, jsonify, Response

from app.models.contract import Contract
from app.models.customer import Customer
from app.models.event import Event
from app.models.user import User
from app.utils import get_current_user

# Create a Blueprint for data-related routes
data_bp = Blueprint("data", __name__)

@data_bp.route("/users", methods=["GET"])
def get_users() -> Union[Response, Tuple[Response, int]]:
    """Retrieve all users from the database"""

    # Verify current user
    user, error = get_current_user()
    if error:
        return error

    # Retrieve all users
    users = User.query.all()

    return jsonify([{"id": user.id,
                     "username": user.username,
                     "email": user.email,
                     "phone": user.phone,
                     "role": str(user.role.value)} for user in users]), HTTPStatus.OK


@data_bp.route("/customers", methods=["GET"])
def get_customers() -> Union[Response, Tuple[Response, int]]:
    """Retrieve all customers from the database"""

    # Verify current user
    user, error = get_current_user()
    if error:
        return error

    # Retrieve all customers from to database
    customers = Customer.query.all()

    return jsonify([{
        "id": customer.id,
        "name": customer.full_name,
        "email": customer.email,
        "company_name": customer.company_name,
        "sales_contact_id": customer.sales_contact_id,
        "last_contact_date": customer.last_contact_date} for customer in customers]), HTTPStatus.OK


@data_bp.route("/contracts", methods=["GET"])
def get_contracts() -> Union[Response, Tuple[Response, int]]:
    """Retrieve all contracts from the database"""

    # Verify current user
    user, error = get_current_user()
    if error:
        return error

    # Retrieve all contracts
    contracts = Contract.query.all()

    return jsonify([{
        "id": contract.id,
        "customer_id": contract.customer_id,
        "sales_contact_id": contract.sales_contact_id,
        "total_amount": contract.total_amount,
        "remaining_amount": contract.remaining_amount,
        "create_at": contract.create_at,
        "update_at": contract.update_at,
        "status": str(contract.status.value)} for contract in contracts]), HTTPStatus.OK


@data_bp.route("/events", methods=["GET"])
def get_events() -> Union[Response, Tuple[Response, int]]:
    """Retrieve all events from the database"""

    # Verify current user
    user, error = get_current_user()
    if error:
        return error

    # Retrieve all events
    events = Event.query.all()

    return jsonify([{
        "id": event.id,
        "name": event.name,
        "status": str(event.status.value),
        "start_date": event.start_date,
        "end_date": event.end_date,
        "location": event.location,
        "attendees": event.attendees,
        "notes": event.notes,
        "create_at": event.create_at,
        "update_at": event.update_at} for event in events]), HTTPStatus.OK
