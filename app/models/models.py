from typing import List
from flask_login import UserMixin
from flask_login.login_manager import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import JSON, DateTime, ForeignKey
from app.extensions import db
from sqlalchemy_serializer import SerializerMixin


class Restaurant(db.Model, SerializerMixin):
    __tablename__ = "restaurants"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    image: Mapped[str]
    cuisine: Mapped[JSON] = mapped_column(type_=JSON, nullable=False)
    rating: Mapped[float]
    deliveryFee: Mapped[float]
    minOrder: Mapped[int]
    isOpen: Mapped[bool]
    zipCodes: Mapped[JSON] = mapped_column(type_=JSON, nullable=False)
    menus: Mapped[List["Menu"]] = relationship(back_populates="restaurant")
    manager: Mapped["User"] = relationship(back_populates="restaurant")
    manager_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    # def __repr__(self) -> str:
    #     return f"Name:{self.name}, Address: {self.address}"


class Menu(db.Model, SerializerMixin):
    __tablename__ = "menus"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[float]
    category: Mapped[str]
    image: Mapped[str]
    available: Mapped[bool]
    restaurant_id = mapped_column(ForeignKey("restaurants.id"))
    restaurant: Mapped["Restaurant"] = relationship(back_populates="menus")

    def __repr__(self) -> str:
        return f"Name:{self.name}, from restaurant: {self.price}"


class Order(db.Model, SerializerMixin):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    items: Mapped[JSON] = mapped_column(type_=JSON, nullable=False)
    status: Mapped[str]
    restaurant_id = mapped_column(ForeignKey("restaurants.id"))
    customer_id = mapped_column(ForeignKey("users.id"))
    restaurant_name: Mapped[str]
    total: Mapped[float]
    user: Mapped["User"] = relationship(back_populates="orders")
    datetime_added: Mapped[datetime] = mapped_column(DateTime)
    note: Mapped[str]
    address_id = mapped_column(ForeignKey("addresses.id"))

    def __repr__(self) -> str:
        return f"Id:{self.id}, from restaurant: {self.restaurant_id} to the address {self.address_id}"


class Address(db.Model, SerializerMixin):
    __tablename__ = "addresses"
    id: Mapped[int] = mapped_column(primary_key=True)
    street: Mapped[str]
    zipCode: Mapped[int]
    user: Mapped["User"] = relationship(back_populates="address")
    user_id = mapped_column(ForeignKey("users.id"))


class User(UserMixin, db.Model, SerializerMixin):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    name: Mapped[str]
    password: Mapped[str]
    role: Mapped[str]
    # address: Mapped[str]
    # zipCode: Mapped[int] = mapped_column(nullable=True)
    balance: Mapped[float]
    orders: Mapped[List["Order"]] = relationship(back_populates="user")
    restaurant: Mapped["Restaurant"] = relationship(back_populates="manager")
    address: Mapped["Address"] = relationship(back_populates="user")
