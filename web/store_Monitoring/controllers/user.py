from flask import Blueprint, request, jsonify
from store_Monitoring import database
from store_Monitoring.models.user import User

user_bp = Blueprint("user_bp", __name__)


@user_bp.route("/signup", methods=["POST"])
def user_signup():
    data = request.get_json()
    email = data["email"].strip().lower()
    uname = data["uname"].strip()
    upass = data["upass"].strip()

    user = database.get_filter_by(User, email=email)

    if user:
        return jsonify(error="Email already exists"), 403
    try:
        database.add_instance(User, email=email, uname=uname, upass=upass)
        return jsonify(message=f"signup process done for {uname}"), 200
    except (ValueError, BaseException) as e:
        return jsonify(error=str(e)), 406


@user_bp.route("/signin", methods=["POST"])
def user_signin():
    data = request.get_json()
    email = data["email"].strip().lower()
    upass = data["upass"].strip()

    user = database.get_filter_by(User, email=email)

    if not user:
        return jsonify(error="No User Found"), 404
    if user.check_password(upass=upass):
        try:
            token = user.encode_auth_token()
            return jsonify(token), 200
        except Exception as e:
            return jsonify(error=str(e)), 400
    return jsonify(error="Credentials are invalid"), 403


@user_bp.route("/token/refresh", methods=["POST"])
def refresh_auth_token():
    """Refreshing auth tokens..."""
    data = request.get_json()
    token = data["token"]
    decode_response = User.decode_auth_token(token)

    if isinstance(decode_response, str):
        return jsonify(error=decode_response), 400

    if decode_response["token_type"] != "refresh":
        return jsonify(error="Please Provide a refresh token"), 403

    user = database.get_filter_by(User, id=decode_response["sub"])

    if not user:
        return jsonify(error="Token is Malformed")

    tokens = user.encode_auth_token()
    return jsonify(tokens)