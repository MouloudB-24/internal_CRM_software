from http import HTTPStatus

from flask import request, jsonify

from app.models.user import User, UserRole


def has_permission(user: User, required_role: UserRole) -> bool:
    """Checks whether the user has the necessary role to perform an action"""

    if user.role == UserRole.MANAGEMENT:
        return True  # Management has all role
    return user.role == required_role


def get_current_user():
    """Retrieve logged-in user from JWT"""

    token = request.headers.get("Authorization")
    if not token:
        return None, (jsonify({"error": "Token missing"}), HTTPStatus.OK)

    user_id = User.verify_token(token)
    if not user_id:
        return None, (jsonify({"error": "Invalid or expired token"}), HTTPStatus.OK)

    user = User.query.get(user_id)
    if not user:
        return None, (jsonify({"error": "User not found"}), HTTPStatus.OK)

    if isinstance(user.role, str):
        user.role = UserRole(user.role)

    return user, None