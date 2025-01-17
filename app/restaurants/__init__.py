from flask import Blueprint, jsonify, request
from flask_login import login_required
from app.extensions import db
from app.models.models import Restaurant, Menu
from population import bool_convertion

restaurants_bp = Blueprint("restaurants", __name__)


# @restaurants_bp.route("/test", methods=["GET"])
# def test():
#     return "Done"


@restaurants_bp.route("/restaurants", methods=["GET", "POST"])
def restaurants_list():
    if request.method == "POST":
        data = request.get_json()[0]
        print(type(data))
        restaurant = Restaurant(
            name=data["name"],
            description=data["description"],
            image=data["image"],
            cuisine=data["cuisine"],
            rating=data["rating"],
            deliveryFee=data["deliveryFee"],
            minOrder=data["minOrder"],
            isOpen=bool_convertion(data["isOpen"]),
            address=data["address"],
            menus=[],
        )

        db.session.add(restaurant)
        db.session.commit()
        return "Restaurant added succefuly"

    restaurants = db.session.execute(db.select(Restaurant)).scalars().fetchall()

    # print("menus", (restaurants[0].menus))
    if restaurants is not None:
        restaurant_list = [
            {
                "id": restaurant.id,
                "name": restaurant.name,
                "description": restaurant.description,
                "image": restaurant.image,
                "cuisine": restaurant.cuisine,
                "rating": restaurant.rating,
                "deliveryFee": restaurant.deliveryFee,
                "minOrder": restaurant.minOrder,
                "isOpen": restaurant.isOpen,
                "address": restaurant.address,
                # "menus": jsonify(restaurant.menus),
            }
            for restaurant in restaurants
        ]
    else:
        restaurant_list = []

    return jsonify(restaurant_list)


# @restaurants_bp.route("/restaurants/create", methods=["POST"])
# def create_restaurant():
#     data = request.get_json()
#     print(type(data))
#     restaurant = Restaurant(name=data["name"], address=data["address"])
#
#     db.session.add(restaurant)
#     db.session.commit()
#     return "Done"


@restaurants_bp.route("/restaurants/<int:id>")
def get_restaurant(id):
    restaurant = db.get_or_404(Restaurant, id)

    if restaurant.menus is not None:
        menu_list = [
            {
                "id": menu.id,
                "name": menu.name,
                "description": menu.description,
                "image": menu.image,
                "category": menu.category,
                # "available": menu.available,
            }
            for menu in restaurant.menus
        ]
    else:
        menu_list = []
    print(restaurant.menus)
    rest = [
        {
            "id": restaurant.id,
            "name": restaurant.name,
            "description": restaurant.description,
            "image": restaurant.image,
            "cuisine": restaurant.cuisine,
            "rating": restaurant.rating,
            "deliveryFee": restaurant.deliveryFee,
            "minOrder": restaurant.minOrder,
            "isOpen": restaurant.isOpen,
            "address": restaurant.address,
            "menus": menu_list,
        }
    ]
    return jsonify(rest)


@restaurants_bp.route("/restaurants/<int:id>", methods=["DELETE"])
@login_required
def delete_restaurant(id):
    restaurant = db.get_or_404(Restaurant, id)

    db.session.delete(restaurant)
    db.session.commit()
    return "Delete Done."


@restaurants_bp.route("/test")
def res_test():
    rest = db.session.execute(
        db.select(Restaurant).where(Restaurant.menus.any(Menu.id == 3))
    ).first()
    print(rest)
    return "Done"
