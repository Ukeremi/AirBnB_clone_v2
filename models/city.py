#!/usr/bin/python3
"""Module that holds the City class"""

import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """Representation of a city"""

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = 'cities'

        name = Column(
            String(128),
            nullable=False
        )

        state_id = Column(
            String(60),
            ForeignKey('states.id'),
            nullable=False
        )

        places = relationship(
            "Place",
            backref="cities",
            cascade="all, delete-orphan"
        )
    else:
        name = ""
        state_id = ""

    def __init__(self, *args, **kwargs):
        """Initializes a city"""
        super().__init__(*args, **kwargs)
