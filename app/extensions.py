from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_socketio import SocketIO


class Base(DeclarativeBase):
    pass


socketio = SocketIO()

db = SQLAlchemy(model_class=Base)
