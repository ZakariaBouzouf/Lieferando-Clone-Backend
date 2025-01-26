from datetime import datetime
from flask import Blueprint, jsonify, request
from flask_login import current_user
from app.extensions import socketio

from app.extensions import db
from app.models.models import Address, Order, Restaurant, User

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
                    "restaurant_name",
                    "total",
                    "datetime_added",
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
    print(orders)
    for order in orders:
        order.customer_name = order.user.name
        address = db.get_or_404(Address, order.address_id)
        order.street = address.street
        order.zipCode = address.zipCode
    result = list(
        map(
            lambda x: x.to_dict(
                only=(
                    "id",
                    "status",
                    "items",
                    "restaurant_id",
                    "customer_id",
                    "total",
                    "datetime_added",
                    "note",
                    "customer_name",
                    "street",
                    "zipCode",
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
        address = Address(
            street=data["street"],
            zipCode=data["zipCode"],
        )

        db.session.add(address)
        db.session.commit()
        order = Order(
            items=data["items"],
            restaurant_id=data["restaurant_id"],
            customer_id=data["customer_id"],
            status=data["status"],
            restaurant_name=data["restaurant_name"],
            total=data["total"],
            datetime_added=datetime.now(),
            note=data["note"],
            address_id=address.id,
        )
        db.session.add(order)
        current_user.balance = current_user.balance - data["total"]
        # restaurant = db.get_or_404(Restaurant, data["restaurant_id"])
        # restaurant.manager.balance = restaurant.manager.balance + data["total"]
        db.session.commit()

        socketio.emit(
            "new_order",
            {
                "customer": current_user.name,
                "total": data["total"],
                "address": data["street"],
                "order_id": order.id,
                "customer_id": data["customer_id"],
                "restaurant_id": data["restaurant_id"],
            },
            namespace="/restaurant_notifications",
        )

        return "Adding done"
    orders = db.session.execute(db.select(Order)).scalars().fetchall()
    print(orders)
    return "Fetching done"


@orders_bp.route("/orders/<int:orderId>/accept", methods=["POST"])
def accept_order(orderId):
    data = request.get_json()
    # db.session.execute(
    #     db.update(Order).where(Order.id == orderId).values(status="accepted")
    # )
    order = db.get_or_404(Order, orderId)
    order.status = "accepted"
    restaurant = db.get_or_404(Restaurant, data["restaurant_id"])
    print(type(order.total))
    restaurant.manager.balance = restaurant.manager.balance + order.total
    db.session.commit()
    return "Done"


@orders_bp.route("/orders/<int:orderId>/decline", methods=["POST"])
def decline_order(orderId):
    data = request.get_json()
    # db.session.execute(
    #     db.update(Order).where(Order.id == orderId).values(status="accepted")
    # )
    order = db.get_or_404(Order, orderId)
    order.status = "declined"
    customer = db.get_or_404(User, data["customer_id"])
    customer.balance = customer.balance + order.total
    db.session.commit()
    return "Done"


# WebSocket event handler
@socketio.on("connect", namespace="/restaurant_notifications")
def handle_connect():
    print("Client connected")


@socketio.on("disconnect", namespace="/restaurant_notifications")
def handle_disconnect():
    print("Client disconnected")


@orders_bp.route("/orders/<int:id>", methods=["PUT"])
def update_order(id):
    data = request.get_json()
    db.session.execute(
        db.update(Order).where(Order.id == id).values(status=data["status"])
    )
    db.session.commit()
    return "Update done"
