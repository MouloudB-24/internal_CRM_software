from http import HTTPStatus
from typing import Union, Tuple

from flask import Blueprint, request, jsonify, Response

from app import db
from app.models.contract import Contract
from app.models.user import UserRole
from app.utils import get_current_user, has_permission

contract_bp = Blueprint("contract", __name__)

@contract_bp.route("/create", methods=["POST"])
def create_contract() -> Union[Response, Tuple[Response, int]]:
    """Create a contract"""

    # Verify current user
    user, error = get_current_user()
    if error:
        return error

    # Permission check: only "Sales" or "Management" users can create contracts
    if not has_permission(user, UserRole.SALES):
        return jsonify({"error": "Permission denied"}), HTTPStatus.OK

    # Retrieve request data
    data = request.get_json()
    customer_id = data.get("customer_id")
    total_amount = data.get("total_amount")
    remaining_amount = data.get("remaining_amount")

    # Validate required fields
    if not all([customer_id, total_amount, remaining_amount]):
        return jsonify({"error": "These fields [customer_id, total_amount and remaining_amount] are required!"}), HTTPStatus.OK

    # Create a new contract
    contract = Contract(
        customer_id=customer_id,
        sales_contact_id=user.id,
        total_amount=total_amount,
        remaining_amount=remaining_amount)

    # # Add the new contract in the database
    db.session.add(contract)
    db.session.commit()

    return jsonify({"message": "Contract created successfully!"}), HTTPStatus.OK


@contract_bp.route("update/<int:contract_id>", methods=["PUT"])
def update_contract(contract_id) -> Union[Response, Tuple[Response, int]]:
    """Update a contract"""

    # Verify current user
    user, error = get_current_user()
    if error:
        return error

    # Permission check: only "Sales" or "Management" users can create contracts
    if not has_permission(user, UserRole.SALES):
        return jsonify({"error": "Permission denied"}), HTTPStatus.OK

    # Find the contract in the database
    contract = Contract.query.get(contract_id)
    if not contract:
        return jsonify({"error": "Contract not found"}), HTTPStatus.OK

    data = request.get_json()
    contract.customer_id = data.get("customer_id", contract.customer_id)
    contract.sales_contact_id = data.get("sales_contact_id", contract.sales_contact_id)
    contract.status = data.get("status", contract.status)
    contract.total_amount = data.get("total_amount", contract.total_amount)
    contract.remaining = data.get("remaining_amount", contract.remaining_amount)

    db.session.commit()
    return jsonify({"message": "Contract update successfully!"}), 200



@contract_bp.route("/delete/<int:contract_id>", methods=["DELETE"])
def delete_customer(contract_id):
    """Delete a contract"""

    # Verify current user
    user, error = get_current_user()
    if error:
        return error

    # Permission check: only "Management" users can delete contracts
    if not has_permission(user, UserRole.MANAGEMENT):
        return jsonify({"error": "Permission denied"}), HTTPStatus.OK

    contract_to_delete = Contract.query.get(contract_id)
    if not contract_to_delete:
        return jsonify({"error": "Contract not found"}), HTTPStatus.OK

    db.session.delete(contract_to_delete)
    db.session.commit()

    return jsonify({"message": "Contract deleted successfully!"}), HTTPStatus.OK
