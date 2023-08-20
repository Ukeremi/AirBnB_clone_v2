#!/usr/bin/python3
"""Module that holds the User class"""

import hashlib
import models
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String


class User(BaseModel, Base):
    """Representation of a User"""

    #if getenv('HBNB_TYPE_STORAGE') == 'db':
    #    __tablename__ = 'users'

    __tablename__ = 'users'
    email = Column(
        String(128),
        nullable=False
    )

    _password = Column(
        'password',
        String(128),
        nullable=False
    )

    first_name = Column(
        String(128),
        nullable=True
    )

    last_name = Column(
        String(128),
        nullable=True
    )

    places = relationship(
        "Place",
        backref="user",
        cascade="all,delete-orphan"
    )

    reviews = relationship(
        "Review",
        backref="user",
        cascade="all, delete-orphan"
    )
    #else:
    #    email = ""
    #    _password = ""
    #    first_name = ""
    #    last_name = ""

    #def __init__(self, *args, **kwargs):
    #    """Initializes User"""
    #    super().__init__(*args, **kwargs)

    #@property
    #def password(self):
    #    """Getter for the password attribute"""
    #    return self._password

    #@password.setter
    #def password(self, pwd):
    #    """Setter for the password attribute, hashes the password"""
    #    self._password = hashlib.md5(pwd.encode()).hexdigest()
