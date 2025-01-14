from flask import Blueprint, request, jsonify
from sqlalchemy import Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# Create a Blueprint for login
login_bp = Blueprint("login", __name__, url_prefix="/auth")

# login_manager = LoginManager()  # Add this line
# login_manager.init_app(app)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    password: Mapped[str]
    createdOn: Mapped[Date]
    isRestaurant: Mapped[bool]


@login_bp.route("/register", methods=["POST"])
def register():
    return "Registration Done"


@login_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()[0]
    email = data["email"]
    password = data["password"]

    # Simple login logic (replace with your actual logic)
    if email == "test@example.com" and password == "password":
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"message": "Invalid credentials"}), 401
