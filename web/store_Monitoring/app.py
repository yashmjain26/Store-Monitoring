

from flask import jsonify
from store_Monitoring import create_app, db
from store_Monitoring.controllers.controller import blueprint
from store_Monitoring.controllers.user import user_bp
app = create_app()


@app.route("/")
def index():
    return jsonify(message="Welcome to store_Monitoring"), 200

app.register_blueprint(blueprint, url_prefix="/")
app.register_blueprint(user_bp, url_prefix="/user")