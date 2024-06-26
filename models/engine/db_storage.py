#!/usr/bin/python3
"""This module defines a class to manage db storage"""
from models.user import User
from models.contact import Contact
from models.base_model import BaseModel ,Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv


class DBStorage:
    """Class Docs"""

    classes = {"User": User, "Contact": Contact}

    __engine = None
    __session = None

    def __init__(self):
        """Function Docs"""
        user = getenv("MYSQL_USER", "dev_user")
        pwd = getenv("MYSQL_PWD", "dev_pwd")
        host = getenv("MYSQL_HOST", "localhost")
        db = getenv("MYSQL_DB", "contact_db")
        env = getenv("ENV", "dev")

        self.__engine = create_engine(
            f"mysql+mysqldb://{user}:{pwd}@{host}/{db}",
            pool_pre_ping=True,
        )

        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def reload(self):
        """ reload method """
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(
            sessionmaker(bind=self.__engine, expire_on_commit=False)
        )
        self.__session = Session()

    def all(self, cls=None):
        """
        query all classes or specific one"""
        allClasses = [User, Contact]
        result = {}
        if cls is not None:
            for obj in self.__session.query(cls).all():
                ClassName = obj.__class__.__name__
                keyName = ClassName + "." + obj.id
                result[keyName] = obj
        else:
            for clss in allClasses:
                for obj in self.__session.query(clss).all():
                    ClassName = obj.__class__.__name__
                    keyName = ClassName + "." + obj.id
                    result[keyName] = obj
        return result

    def new(self, obj):
        """add new obj"""
        if obj:
            self.__session.add(obj)

    def save(self):
        """commit all changes"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session"""
        if obj:
            self.__session.delete(obj)
    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        """query on the current database session"""
        if cls:
            obj = self.__session.query(cls).get(id)
            return obj
        return None

    def count(self, cls=None):
        """Returns the number of objects in storage matching the given class"""
        if cls:
            all_objs_dict = self.all(cls)
            count = len(all_objs_dict)
        else:
            count = len(self.all())
        return count