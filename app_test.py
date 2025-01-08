from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import inspect

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
    address: Mapped[str]

    def __repr__(self) -> str:
        return f"Name:{self.name}, Address: {self.address}"


with app.app_context():
    db.drop_all()
    db.create_all()
    restau1 = Restaurant(name="mcdo", address="marjan")
    restau2 = Restaurant(name="jambo", address="houria")
    inspector = inspect(db.engine)
    columns = inspector.get_columns("restaurant")
    print(columns)
    print(f"this is a resto :{restau1}")

    db.session.add(restau1)
    db.session.add(restau2)
    db.session.commit()


@app.route("/")
def index():
    return "Testing 123"


@app.route("/restaurants")
def restaurants_list():
    # restaurants = [
    #     {"id": 1, "name": "Mcdo", "address": "Houria 3"},
    #     {"id": 2, "name": "Jambo", "address": "Houria 3"},
    # ]
    restaurants = db.session.execute(db.select(Restaurant)).scalars().fetchall()
    # print(type(restaurants[0]))
    # print(f"This is the first element {restaurants[0]}")
    # restaurants = Restaurant.query.all()
    # print(f"this is the restaurants : {restaurants}")
    if restaurants is not None:
        restaurant_list = [
            {
                "id": restaurant.id,
                "name": restaurant.name,
                "address": restaurant.address,
            }
            for restaurant in restaurants
        ]
    else:
        restaurant_list = []

    # print(f"restau : {restaurant_list}")
    # return f"done : {restaurants}"
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
