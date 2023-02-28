from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
import os
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    """Application-Factory Method"""

    flask_app = Flask(__name__)
    
    app_settings = os.getenv("APP_SETTINGS", "store_Monitoring.config.Config")
    flask_app.config.from_object(app_settings)

    # flask_app.config.from_object()

    db.init_app(flask_app)
    migrate.init_app(flask_app, db)
    CORS(flask_app)
    flask_app.app_context().push()

    
    return flask_app