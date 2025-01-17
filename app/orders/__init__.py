from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models.models import Order

orders_bp = Blueprint("orders", __name__)


@orders_bp.route("/testorders")
def testt():
    return "works"


@orders_bp.route("/orders/<int:id>/customer")
def customer_order(id):
    print("id", id)
    orders = (
        db.session.execute(db.select(Order).where(Order.customer_id == id))
        .scalars()
        .fetchall()
    )
    result = list(
        map(
            lambda x: x.to_dict(
                only=(
                    "id",
                    "status",
                    "items",
                    "restaurant_id",
                    "customer_id",
                    "restaurant",
                    # "created_date",
                )
            ),
            orders,
        )
    )

    print(result)

    return jsonify(result), 200


@orders_bp.route("/orders/<int:id>/restaurant")
def restaurant_order(id):
    print("id", id)
    orders = (
        db.session.execute(db.select(Order).where(Order.restaurant_id == id))
        .scalars()
        .fetchall()
    )
    result = list(
        map(
            lambda x: x.to_dict(
                only=(
                    "id",
                    "status",
                    "items",
                    "restaurant_id",
                    "customer_id",
                    "restaurant",
                    # "created_date",
                )
            ),
            orders,
        )
    )

    print(result)

    return jsonify(result), 200


@orders_bp.route("/orders", methods=["GET", "POST"])
def add_order():
    if request.method == "POST":
        data = request.get_json()
        print(data)
        order = Order(
            items=data["items"],
            restaurant_id=data["restaurant_id"],
            customer_id=data["customer_id"],
            status=data["status"],
            restaurant=data["restaurant"],
            # created_date=data["created_date"],
        )
        db.session.add(order)
        db.session.commit()

        return "Adding done"
    orders = db.session.execute(db.select(Order)).scalars().fetchall()
    print(orders)
    return "Fetching done"


@orders_bp.route("/orders/<int:id>", methods=["PUT"])
def update_order(id):
    data = request.get_json()
    db.session.execute(
        db.update(Order).where(Order.id == id).values(status=data["status"])
    )
    db.session.commit()
    return "Update done"
