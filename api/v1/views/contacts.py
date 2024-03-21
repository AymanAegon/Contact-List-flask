#!/usr/bin/python3
"""define routes of blueprint
"""

from api.v1.views import app_views
from models import storage
from models.user import User
from models.contact import Contact


@app_views.route("/contacts", strict_slashes=False, methods=["GET"])
def contacts():
    contacts = storage.all(Contact)
    return contacts

@app_views.route("/contact", strict_slashes=False, methods=["GET"])
def add_contact():
    new_contact = Contact(
        first_name="test",
        last_name="TEST",
        email="test@email.com"
    )
    return new_contact.to_dict()