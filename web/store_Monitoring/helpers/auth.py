from functools import wraps
from flask import request, make_response, jsonify

# from project import database
from store_Monitoring.models.user import User


def is_authenticated(fuc):
    @wraps(fuc)
    def wrapped(*args, **kwargs):
        prefix = "user access"
        auth_token = None
        responseObj = {"status": "failed", "message": "Not authorized"}

        auth_header = request.headers.get("Authorization")

        if auth_header:
            try:
                prefix, auth_token = auth_header.split()
                responseObj["message"] = f"{prefix} token is malformed"
            except Exception:
                return make_response(jsonify(responseObj)), 401

        if not auth_token:
            return make_response(jsonify(responseObj)), 401

        decode_response = User.decode_auth_token(auth_token)

        if isinstance(decode_response, str):
            responseObj["message"] = decode_response
            return make_response(jsonify(responseObj)), 401

        if decode_response["token_type"] != "access":
            return make_response(jsonify(responseObj)), 401

        uid = decode_response["sub"]
        curr_user = None
        if isinstance(uid, int):
            curr_user = database.get_filter_by(User, id=uid)

        return fuc(curr_user=curr_user, *args, **kwargs)

    return wrapped