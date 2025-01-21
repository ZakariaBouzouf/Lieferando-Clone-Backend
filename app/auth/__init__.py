from flask import Blueprint, redirect, request, jsonify
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from app.extensions import db
from population import bool_convertion
from app.models.models import Restaurant, User

# Create a Blueprint for login
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


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
    if data["role"] == "customer":
        new_user.balance = 100
    else:
        new_user.balance = 0
        restaurant = Restaurant(
            name=data["name"],
            description=data["description"],
            image=data["image"],
            cuisine=data["cuisine"],
            minOrder=data["minOrder"],
            isOpen=bool_convertion(data["isOpen"]),
            address=data["address"],
            deliveryFee=data["deliveryFee"],
            rating=0,
            menus=[],
            manager=new_user,
            zipCodes=data["zipCodes"],
        )
        db.session.add(restaurant)
        # new_user.restaurant(restaurant)

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
        if user.role == "restaurant":
            return (
                jsonify(
                    {
                        "message": "Login successful",
                        "userId": user.id,
                        "role": user.role,
                        "name": user.name,
                        "balance": user.balance,
                        "restaurantId": user.restaurant.id,
                    }
                ),
                200,
            )
        else:
            return (
                jsonify(
                    {
                        "message": "Login successful",
                        "userId": user.id,
                        "role": user.role,
                        "name": user.name,
                        "balance": user.balance,
                        "zipCode": user.zipCode,
                    }
                ),
                200,
            )

    return jsonify({"message": "Invalid credentials"}), 401
    # Simple login logic (replace with your actual logic)


@auth_bp.route("/logout")
@login_required
def logout():
    response = logout_user()
    print(response)
    return jsonify({"message": "Logout done"}), 200


@auth_bp.route("/session", methods=["GET"])
@login_required
def get_session():
    print(current_user)
    if current_user.role == "restaurant":
        return (
            jsonify(
                {
                    "userId": current_user.id,
                    "email": current_user.email,
                    "role": current_user.role,
                    "balance": current_user.balance,
                    "restaurantId": current_user.restaurant.id,
                    "name": current_user.name,
                }
            ),
            200,
        )

    return (
        jsonify(
            {
                "userId": current_user.id,
                "email": current_user.email,
                "role": current_user.role,
                "balance": current_user.balance,
                "name": current_user.name,
                "zipCode": current_user.zipCode,
            }
        ),
        200,
    )


@auth_bp.route("/balance_check", methods=["POST"])
def check_balance():
    total = request.get_json()["total"]
    print(total, current_user.balance)
    if current_user.balance >= total:
        return jsonify({"message": "Enough"}), 200
    return jsonify({"message": "Not enough"}), 400
