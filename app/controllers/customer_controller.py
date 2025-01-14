from http import HTTPStatus
from typing import Union, Tuple

from flask import Blueprint, jsonify, request, Response

from app import db
from app.models.customer import Customer
from app.models.user import UserRole
from app.utils import get_current_user, has_permission

customer_bp = Blueprint("customer", __name__)

@customer_bp.route("/create", methods=["POST"])
def create_customer() -> Union[Response, Tuple[Response, int]]:
    """Create a customer in the database"""

    # Verify the current user
    user, error = get_current_user()
    if error:
        return error

    # Permission check: only "Sales" or "Management" users can create customers
    if not has_permission(user, UserRole.SALES):
        return jsonify({"error": "Permission denied"}), HTTPStatus.OK

    # Retrieve request data
    data = request.get_json()
    full_name = data.get("full_name")
    email = data.get("email")
    phone = data.get("phone")
    company_name = data.get("company_name")
    last_contact_date = data.get("last_contact_date")

    # Validate required fields
    if not all([full_name, email, phone]):
        return jsonify({"error": "These fields [full_name, email and phone] are required!"}), HTTPStatus.OK

    # Check if the email is present in the database
    if Customer.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), HTTPStatus.OK

    # Create a new customer
    customer = Customer(
        full_name=full_name,
        email=email,
        phone=phone,
        company_name=company_name,
        last_contact_date=last_contact_date,
        sales_contact_id=user.id)

    # Add the new customer in the database
    db.session.add(customer)
    db.session.commit()

    return jsonify({"message": "Customer created successfully!"}), HTTPStatus.OK


@customer_bp.route("/update/<int:customer_id>", methods=["PUT"])
def update_customer(customer_id) -> Union[Response, Tuple[Response, int]]:
    """Update customer data in the database"""

    # Verify the current user
    user, error = get_current_user()
    if error:
        return error

    # Permission check: only "Sales" or "Management" users can update customers data
    if not has_permission(user, UserRole.SALES):
        return jsonify({"error": "Permission denied"}), HTTPStatus.OK

    # Find the customer in the database
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({"error": "Customer not found"}), HTTPStatus.OK

    #  Check that customer belongs to the user
    if customer.sales_contact_id != user.id and user.role != UserRole.MANAGEMENT:
        return jsonify({"error": "Permission denied"}), HTTPStatus.OK

    # Retrieve request data
    data = request.get_json()
    customer.full_name = data.get("full_name", customer.full_name)
    customer.email = data.get("email", customer.email)
    customer.phone = data.get("phone", customer.phone)
    customer.company_name = data.get("company_name", customer.company_name)
    customer.last_contact_date = data.get("last_contact_date", customer.last_contact_date)

    # Update customer data in the database
    db.session.commit()
    return jsonify({"message": "Customer updated successfully!"}), HTTPStatus.OK


@customer_bp.route("/delete/<int:customer_id>", methods=["DELETE"])
def delete_customer(customer_id) -> Union[Response, Tuple[Response, int]]:
    """Delete the customer from the database"""

    # Verify current user
    user, error = get_current_user()
    if error:
        return error

    # Permission check: only "Management" users can delete customers from the database
    if not has_permission(user, UserRole.MANAGEMENT):
        return jsonify({"error": "Permission denied"}), HTTPStatus.OK

    # Find the customer in the database
    customer_to_delete = Customer.query.get(customer_id)
    if not customer_to_delete:
        return jsonify({"error": "Customer not found"}), HTTPStatus.OK

    # Delete the customer from the database
    db.session.delete(customer_to_delete)
    db.session.commit()

    return jsonify({"message": "Customer deleted successfully!"}), HTTPStatus.OK
