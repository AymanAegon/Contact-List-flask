#!/usr/bin/python3
"""
a class User that inherits from BaseModel:
"""
from sqlalchemy import Column, String, ForeignKey
from models.base_model import BaseModel, Base
import models


class Contact(BaseModel, Base):
    """
    User class
    """
    if models.StorageType == 'db':
        __tablename__ = "contacts"
        first_name = Column(String(40), nullable=False)
        last_name = Column(String(40), nullable=False)
        email = Column(String(128), nullable=False)
        user_id = Column(String(128), ForeignKey("users.id"), nullable=False)

    else:
        first_name = ''
        last_email = ''
        email = ''
        user_id = ''

    def __init__(self, *args, **kwargs):
        """initializes state"""
        super().__init__(*args, **kwargs)