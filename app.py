from typing import List
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import JSON, ForeignKey, inspect
from sqlalchemy.sql.sqltypes import ARRAY
from population import mock_data
import json

# My app
app = Flask(__name__)


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"

db.init_app(app)


class Restaurant(Base):
    __tablename__ = "restaurant"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    image: Mapped[str]
    cuisine: Mapped[JSON] = mapped_column(type_=JSON, nullable=False)
    rating: Mapped[float]
    deliveryFee: Mapped[float]
    minOrder: Mapped[int]
    isOpen: Mapped[bool]
    address: Mapped[str]
    menus: Mapped[List["Menu"]] = relationship(back_populates="restaurant")

    def __repr__(self) -> str:
        return f"Name:{self.name}, Address: {self.address}"


class Menu(Base):
    __tablename__ = "menu"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[float]
    category: Mapped[str]
    image: Mapped[str]
    restaurant_id = mapped_column(ForeignKey("restaurant.id"))
    available: Mapped[bool]
    restaurant: Mapped["Restaurant"] = relationship(back_populates="menus")


def populate_database(data):
    for restaurant_data in data:
        # Create a Restaurant object
        restaurant = Restaurant(
            name=restaurant_data["name"],
            description=restaurant_data["description"],
            image=restaurant_data["image"],
            cuisine=json.dumps(restaurant_data["cuisine"]),
            rating=restaurant_data["rating"],
            delivery_fee=restaurant_data["deliveryFee"],
            min_order=restaurant_data["minOrder"],
            is_open=restaurant_data["isOpen"],
            address=restaurant_data["address"],
            menu=[],
        )

        # Add menu items
        for menu_data in restaurant_data["menu"]:
            menu_item = Menu(
                name=menu_data["name"],
                description=menu_data["description"],
                price=menu_data["price"],
                category=menu_data["category"],
                image=menu_data["image"],
                available=menu_data["available"],
                restaurant_id=restaurant.id,
            )
            db.session.add(menu_item)
        db.session.add(restaurant)

    db.session.commit()
    print("Database populated successfully!")


with app.app_context():
    db.drop_all()
    db.create_all()
    # populate_database(mock_data)
    menu1 = Menu(
        name="Margherita Pizza",
        description="Fresh tomatoes, mozzarella, basil",
        price=14.99,
        category="Pizza",
        image="https://images.unsplash.com/photo-1574071318508-1cdbab80d002",
        restaurant_id=1,
        available=True,
    )
    restau1 = Restaurant(
        name="Pizza Paradise",
        description="Authentic Italian pizzas and pasta",
        image="https://images.unsplash.com/photo-1604382354936-07c5d9983bd3",
        cuisine=["Italian", "Pizza"],
        rating=4.5,
        deliveryFee=0,
        minOrder=15,
        isOpen=True,
        address="123 Main st",
        menus=[menu1],
    )
    # restau1 = Restaurant(name="mcdo", address="marjan")
    # restau2 = Restaurant(name="jambo", address="houria")
    # inspector = inspect(db.engine)
    # columns = inspector.get_columns("restaurant")
    # print(columns)
    # print(f"this is a resto :{restau1}")
    db.session.add(restau1)
    db.session.add(menu1)
    # db.session.add(restau2)
    db.session.commit()


@app.route("/")
def index():
    return "Testing 123"


@app.route("/restaurants")
def restaurants_list():
    restaurants = db.session.execute(db.select(Restaurant)).scalars().fetchall()

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
            }
            for restaurant in restaurants
        ]
    else:
        restaurant_list = []

    return jsonify(restaurant_list)


@app.route("/restaurants/create", methods=["POST"])
def create_restaurant():
    data = request.get_json()[0]
    print(type(data))
    restaurant = Restaurant(name=data["name"], address=data["address"])

    db.session.add(restaurant)
    db.session.commit()
    return "Done"


@app.route("/restaurants/<int:id>")
def get_restaurant(id):
    restaurant = db.get_or_404(Restaurant, id)

    rest = [
        {"id": restaurant.id, "name": restaurant.name, "address": restaurant.address}
    ]
    return jsonify(rest)


@app.route("/restaurants/<int:id>", methods=["DELETE"])
def delete_restaurant(id):
    restaurant = db.get_or_404(Restaurant, id)

    db.session.delete(restaurant)
    db.session.commit()
    return "Delete Done."


if __name__ in "__main__":
    app.run(debug=True)
