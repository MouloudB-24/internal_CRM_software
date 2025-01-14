from http import HTTPStatus
from typing import Tuple, Union

from flask import Blueprint, request, jsonify, Response

from app import db
from app.models.user import User, UserRole
from app.utils import get_current_user, has_permission

user_bp = Blueprint("user", __name__)


@user_bp.route("/token", methods=["POST"])
def login() -> Tuple[Response, int]:
    """Authenticate user and generate JWT token"""

    # Retrieve request data
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # Validate required fields
    if not username or not password:
        return jsonify({"error": "These fields [username and password] are required!"}), HTTPStatus.OK

    # Checks if a user exists and validate the password
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), HTTPStatus.OK

    # Generate a JWT token
    token = user.generate_token()
    return jsonify({"token": token, "role": user.role.value}), HTTPStatus.OK


@user_bp.route('/refresh', methods=['POST'])
def refresh_token() -> Tuple[Response, int]:
    """Refresh the JWT token"""

    # Retrieve the JWT token from the request http
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"error": "Token missing"}), HTTPStatus.OK

    # Retrieve user id by decoding token
    user_id = User.verify_token(token)
    if not user_id:
        return jsonify({"error": "Invalid or expired token"}), HTTPStatus.OK

    # Find the user in the database
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), HTTPStatus.OK

    # Generate a new token
    new_token = user.generate_token()
    return jsonify({"token": new_token}), HTTPStatus.OK


@user_bp.route("/create", methods=["POST"])
def create_user() -> Union[Response, Tuple[Response, int]]:
    """Create a new user"""
    # Verify current user
    user, error = get_current_user()
    if error:
        return error

    # Permission check: only "Management" users can create users
    if not has_permission(user, UserRole.MANAGEMENT):
        return jsonify({"error": "Permission denied!"}), HTTPStatus.OK


    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), HTTPStatus.OK

    # Retrieve and Validate data
    username = data.get("username")
    email = data.get("email")
    phone = data.get("phone")
    password = data.get("password")
    role = data.get("role")

    # Validation des champs requis
    if not all([username, email, password, role]):
        return jsonify({"error": "These fields [username, password, email, phone and role] are required!"}), HTTPStatus.OK

    # Check role
    try:
        role_enum = UserRole(role)
    except ValueError:
        return jsonify({"error": f"Invalid role. Valid roles are: {[role.value for role in UserRole]}"}), HTTPStatus.OK

    # Check username and email uniqueness
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), HTTPStatus.OK
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), HTTPStatus.OK

    # Create a new user and add it to the database
    try:
        user = User(username=username, email=email, phone=phone, role=role_enum)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        return jsonify({"message": "User created successfully"}), HTTPStatus.OK

    except Exception as e:
        # Cancel modification and return to previous state
        db.session.rollback()
        return jsonify({"error": f"Database error: {str(e)}"}), HTTPStatus.OK


@user_bp.route("/update/<int:user_id>", methods=["PUT"])
def update_user(user_id) -> Union[Response, Tuple[Response, int]]:
    """Update a user"""

    # Verify current user
    user, error = get_current_user()
    if error:
        return error

    # Permission check: only "Management" users can create users
    if not has_permission(user, UserRole.MANAGEMENT):
        return jsonify({"error": "Permission denied!"}), HTTPStatus.OK

    # Find the user in the database
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), HTTPStatus.OK

    data = request.get_json()
    user.username = data.get("username", user.username)
    user.email = data.get("email", user.email)
    user.phone = data.get("phone", user.phone)

    role = data.get("role")
    if role:
        try:
            user.role = UserRole(role)
        except ValueError:
            return jsonify({"error": f"Invalid role. Valid roles: {[role.value for role in UserRole]}"}), HTTPStatus.OK

    db.session.commit()
    return jsonify({"message": "Collaborator updated successfully!"})


@user_bp.route("/delete/<int:user_id>", methods=["DELETE"])
def delete_user(user_id) -> Union[Response, Tuple[Response, int]]:
    """Delete a user from the database"""

    # Verify current user
    user, error = get_current_user()
    if error:
        return error

    # Permission check: only "Management" users can create users
    if not has_permission(user, UserRole.MANAGEMENT):
        return jsonify({"error": "Permission denied"}), HTTPStatus.OK

    # Find the user in the database
    user_to_delete = User.query.get(user_id)
    if not user_to_delete:
        return jsonify({"error": "User not found"}), HTTPStatus.OK

    db.session.delete(user_to_delete)
    db.session.commit()
    return jsonify({"message": "User deleted successfully!"}), HTTPStatus.OK




