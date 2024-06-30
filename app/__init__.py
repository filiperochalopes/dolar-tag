from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    Session(app)

    from .routes import routes
    app.register_blueprint(routes)

    with app.app_context():
        db.create_all()
    
    return app