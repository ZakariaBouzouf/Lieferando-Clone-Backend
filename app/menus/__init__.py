from flask import Blueprint, jsonify, request
from app.extensions import db

from app.models.models import Menu, Restaurant


menus_bp = Blueprint("menus", __name__)


@menus_bp.route("/menu/<int:restaurantId>")
def get_menus(restaurantId):
    restaurant = db.get_or_404(Restaurant, restaurantId)
    # print(type(bool_convertion(restaurant.menus[0].available)))
    # print(bool_convertion(restaurant.menus[0].available))
    if restaurant.menus is not None:
        menu_list = [
            {
                "id": menu.id,
                "name": menu.name,
                "description": menu.description,
                "image": menu.image,
                "category": menu.category,
                "price": menu.price,
                "available": menu.available,
            }
            for menu in restaurant.menus
        ]
    else:
        menu_list = []

    return jsonify(menu_list)


@menus_bp.route("/menu/<int:restaurantId>", methods=["POST"])
def add_menu(restaurantId):
    if request.method == "POST":
        data = request.get_json()
        print(data)
        menu = Menu(
            name=data["name"],
            description=data["description"],
            price=data["price"],
            category=data["category"],
            image=data["image"],
            available=data["available"],
        )
        # We need this connection to specify who is the restaurant
        restaurant = db.get_or_404(Restaurant, restaurantId)
        restaurant.menus.append(menu)
        db.session.add(menu)
        db.session.commit()
        return jsonify(
            menu.to_dict(
                only=(
                    "name",
                    "description",
                    "price",
                    "category",
                    "id",
                    "available",
                    "image",
                )
            )
        )
    return "Somethis when wrong"


@menus_bp.route("/menu/<int:menuId>", methods=["PUT", "DELETE"])
def managing_menu(menuId):
    if request.method == "DELETE":
        menu = db.get_or_404(Menu, menuId)

        db.session.delete(menu)
        db.session.commit()
        return "Delete Done."
    elif request.method == "PUT":
        data = request.get_json()
        db.session.execute(
            db.update(Menu)
            .where(Menu.id == menuId)
            .values(
                name=data["name"],
                description=data["description"],
                price=data["price"],
                category=data["category"],
                image=data["image"],
                available=data["available"],
            )
        )
        db.session.commit()
        return "Update Done."

    return "done"
