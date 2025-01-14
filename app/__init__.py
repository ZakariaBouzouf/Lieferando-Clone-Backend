from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_cors import CORS

from app.extensions import db
from app.auth import auth_bp
from app.restaurants import restaurants_bp
from config import Config
from population import populate_database
from app.models.models import User


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    with app.app_context():
        db.drop_all()
        # from app.models.models import Restaurant, Menu

        db.create_all()
        populate_database()

    CORS(
        app,
        supports_credentials=True,
    )
    # app.config["CORS_HEADERS"] = "Content-Type"

    app.register_blueprint(auth_bp)
    app.register_blueprint(restaurants_bp)

    # Important to manage the sessions for users
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter_by(id=user_id).first()

    return app
