#!/usr/bin/python3
"""Module that holds the State class"""

import models
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """Representation of a State"""

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = 'states'

        name = Column(
            String(128),
            nullable=False
        )

        cities = relationship(
            "City",
            cascade="all,delete",
            backref="states"
        )
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """Initializes State"""
        super().__init__(*args, **kwargs)

    if getenv('HBNB_TYPE_STORAGE') != 'db':
        @property
        def cities(self):
            """Getter attribute that returns City instances"""
            values_city = models.storage.all("City").values()

            list_city = [
                city
                for city in values_city
                if city.state_id == self.id
            ]
            return list_city
