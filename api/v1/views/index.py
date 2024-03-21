#!/usr/bin/python3
"""define routes of blueprint
"""

from api.v1.views import app_views
from models import storage
from models.user import User
from models.contact import Contact


@app_views.route("/status", strict_slashes=False, methods=["GET"])
def status():
    return {
        "status": "OK",
    }


@app_views.route("/stats", strict_slashes=False, methods=["GET"])
def stats():
    contacts = storage.count(Contact)
    users = storage.count(User)

    return {
        "contacts": contacts,
        "users": users
    }