from flask import Blueprint, redirect, request, jsonify
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from app.extensions import db
from population import bool_convertion
from app.models.models import User

# Create a Blueprint for login
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


# class Base(DeclarativeBase):
#     pass
#


@auth_bp.route("/signup", methods=["POST"])
def register():
    data = request.get_json()
    print(data)
    new_user = User(
        email=data["email"],
        name=data["name"],
        password=data["password"],
        role=data["role"],
        address=data["address"],
    )

    # TODO: Check if the email already exist in the Database

    db.session.add(new_user)
    db.session.commit()
    return "Registration Done"


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    print(data)

    email = data["email"]
    password = data["password"]
    # #
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "Email does not exist."}), 401
    if user.password == password:
        login_user(user)
        return (
            jsonify(
                {"message": "Login successful", "userId": user.id, "role": user.role}
            ),
            200,
        )

    return jsonify({"message": "Invalid credentials"}), 401
    # Simple login logic (replace with your actual logic)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout done"}), 200


@auth_bp.route("/session", methods=["GET"])
@login_required
def get_session():
    return (
        jsonify(
            {
                "userId": current_user.id,
                "email": current_user.email,
                "role": current_user.role,
            }
        ),
        200,
    )
