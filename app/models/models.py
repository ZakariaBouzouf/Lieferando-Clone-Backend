from flask_login import UserMixin
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import JSON, ForeignKey
from typing import List
from app.extensions import db


class Base(DeclarativeBase):
    pass


class Restaurant(db.Model):
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


class Menu(db.Model):
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

    def __repr__(self) -> str:
        return f"Name:{self.name}, from restaurant: {self.price}"


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    name: Mapped[str]
    password: Mapped[str]
    role: Mapped[str]
    address: Mapped[str]
    # createdOn: Mapped[Date]
    # self.created_on = datetime.now()
    # created_on = db.Column(db.DateTime, nullable=False)
