#!/usr/bin/python3
"""
a class User that inherits from BaseModel:
"""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models.contact import Contact
import models
from flask_login import UserMixin

if models.StorageType == 'db':
    User_mixin = UserMixin
else:
    User_mixin = object

class User(UserMixin, BaseModel, Base):
    """
    User class
    """
    if models.StorageType == 'db':
        __tablename__ = "users"
        name = Column(String(128), nullable=False)
        email = Column(String(128), unique=True, nullable=False)
        password = Column(String(256), nullable=False)
        contacts = relationship("Contact", cascade="all,delete", backref="user")

    else:
        name = ''
        email = ''
        password = ''

    def __init__(self, *args, **kwargs):
        """initializes state"""
        super().__init__(*args, **kwargs)

    if models.StorageType != "db":
        @property
        def contacts(self):
            """getter for list of contacts instances related to the user"""
            contact_list = []
            all_contacts = models.storage.all(Contact)
            for contact in all_contacts.values():
                if contact.user_id == self.id:
                    contact_list.append(contact)
            return contact_list

    # __hash__ = object.__hash__

    # @property
    # def is_active(self):
    #     return True

    # @property
    # def is_authenticated(self):
    #     return self.is_active

    # @property
    # def is_anonymous(self):
    #     return False

    def get_id(self):
        try:
            return str(self.id)
        except AttributeError:
            raise NotImplementedError("No `id` attribute - override `get_id`") from None

    # def __eq__(self, other):
    #     """
    #     Checks the equality of two `UserMixin` objects using `get_id`.
    #     """
    #     if isinstance(other, UserMixin):
    #         return self.get_id() == other.get_id()
    #     return NotImplemented

    # def __ne__(self, other):
    #     """
    #     Checks the inequality of two `UserMixin` objects using `get_id`.
    #     """
    #     equal = self.__eq__(other)
    #     if equal is NotImplemented:
    #         return NotImplemented
    #     return not equal