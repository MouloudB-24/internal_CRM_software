from flask import Blueprint, request, jsonify
from app.models.user import User
from app.models.department import Departement
from app import db


user_dp = Blueprint("user", __name__)

@user_dp.route("/register", methods=["POST"])
def register_user():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    phone = data.get("phone")
    password = data.get("password")
    department_id = data.get("department_id")

    if not all([username, email, password, phone, department_id]):
        return jsonify({"error": "Missing fields"}), 400

    # Verifie si l'email est déjà utilisé
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 400

    # Creation de l'utilisateur
    user = User(username=username, email=email, phone=phone, department_id=department_id)

    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully👏"})


@user_dp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Missing email or password"})

    # vérifier si un user existe
    user = User.query.filter_by(email=email).first()
    if not user or user.check_password(password):
        return jsonify({"error": "Invalid credentials"})

    # Générer un jeton JWT
    token = user.generate_token()
    return jsonify({"token": token}), 200