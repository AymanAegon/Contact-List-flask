#!/usr/bin/python3
"""define routes of blueprint
"""

from api.v1.views import app_views
from models import storage
from models.user import User
from models.contact import Contact
from flask import jsonify, request


@app_views.route("/users", strict_slashes=False, methods=["GET"])
def users():
    users = storage.all(User).values()
    result = []
    for value in users:
        result.append(value.to_dict())
    return {"users": result}

@app_views.route("/user", strict_slashes=False, methods=["GET"])
def add_user():
    new_user = User(
        name=request.json.get("name"),
        email=request.json.get("email"),
        password=request.json.get("password")
    )
    new_user.save()
    return new_user.to_dict()