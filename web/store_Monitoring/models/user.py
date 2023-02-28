import jwt
import datetime

from store_Monitoring import db
from werkzeug.security import generate_password_hash, check_password_hash

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import validates

import os

SECRET_KEY = os.environ.get("SECRET_KEY", "SOME_SECRET_KEY")


class User(db.Model):
    """User Model for Handling user information."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True, nullable=False)
    uname = Column(String(50), nullable=False)
    upass = Column(String(255), nullable=False)
    is_active = Column(Boolean(), default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    # projects = db.relationship("Projects", backref="projects", lazy=True)

    def __init__(self, email, uname, upass):
        self.email = email
        self.uname = uname
        self.set_password(upass)

    def __repr__(self) -> str:
        return str(f"<User {self.id}:{self.email}>")

    @validates("email")
    def validate_email(self, key, email):
        """Email validation function"""
        if "@" not in email:
            raise ValueError(f"{key} Invalid email address")
        return email

    def set_password(self, upass):
        """Creates a Secure Hash Password"""
        if len(upass) < 6:
            raise ValueError(f"Password lenth is {len(upass)} and it must be at least 6 characters long")
        self.upass = generate_password_hash(upass, method="sha256")

    def check_password(self, upass):
        """Checks the stored Password"""
        return check_password_hash(self.upass, upass)

    def encode_auth_token(self):
        """Encodes the auth_tokens
        :token_type: access, refresh"""
        try:

            access_payload = {
                "token_type": "access",
                "iat": datetime.datetime.utcnow(),
                "exp": datetime.datetime.utcnow()
                + datetime.timedelta(days=0, minutes=20),
                "sub": self.id,
                "email": self.email,
            }
            refresh_payload = {
                "token_type": "refresh",
                "iat": datetime.datetime.utcnow(),
                "exp": datetime.datetime.utcnow() + datetime.timedelta(days=0, hours=3),
                "sub": self.id,
                "email": self.email,
            }
            access_token = jwt.encode(access_payload, SECRET_KEY, algorithm="HS256")
            refresh_token = jwt.encode(refresh_payload, SECRET_KEY, algorithm="HS256")
            return {"access": access_token, "refresh": refresh_token}
        except Exception as e:
            print("Could not Encode Auth token", e)
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """Decode auth token"""
        try:
            payload = jwt.decode(auth_token, SECRET_KEY, algorithms="HS256")
            return payload
        except jwt.ExpiredSignatureError:
            return "Signature/ Token expired, Signin Again"
        except jwt.InvalidTokenError:
            return "Invalid Token, Signin Again"