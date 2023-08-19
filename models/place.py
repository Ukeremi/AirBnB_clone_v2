#!/usr/bin/python3
"""Module that holds the Place class"""

import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer, Table, Float, ForeignKey
from sqlalchemy.orm import relationship

# Define the association table for the many-to-many relationship
# between Place and Amenity
if getenv('HBNB_TYPE_STORAGE') == 'db':
    place_amenity = Table(
        'place_amenity',
        Base.metadata,
        Column(
            'place_id',
            String(60),
            ForeignKey('places.id'),
            primary_key=True,
            nullable=False
        ),
        Column(
            'amenity_id',
            String(60),
            ForeignKey('amenities.id'),
            primary_key=True,
            nullable=False
        )
    )


class Place(BaseModel, Base):
    """Representation of Place"""

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = 'places'

        city_id = Column(
            String(60),
            ForeignKey("cities.id"),
            nullable=False
        )

        user_id = Column(
            String(60),
            ForeignKey('users.id'),
            nullable=False
        )

        name = Column(
            String(128),
            nullable=False
        )

        description = Column(
            String(1024),
            nullable=True
        )

        number_rooms = Column(
            Integer,
            default=0,
            nullable=False
        )

        number_bathrooms = Column(
            Integer,
            default=0,
            nullable=False
        )

        max_guest = Column(
            Integer,
            default=0,
            nullable=False
        )

        price_by_night = Column(
            Integer,
            default=0,
            nullable=False
        )

        latitude = Column(
            Float,
            nullable=True
        )

        longitude = Column(
            Float,
            nullable=True
        )

        # Define a one-to-many relationship with Review
        reviews = relationship(
            "Review",
            cascade="all, delete",
            backref="places"
        )

        # Define a many-to-many relationship with Amenity
        amenities = relationship(
            "Amenity",
            secondary='place_amenity',
            viewonly=False,
            backref="place_amenities"
        )

    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0

    def __init__(self, *args, **kwargs):
        """Initializes Place"""
        super().__init__(*args, **kwargs)

    @property
    def reviews(self):
        """Attribute that returns a list of Review instances"""
        values_review = models.storage.all("Review").values()
        list_review = [
            review
            for review in values_review
            if review.place_id == self.id
        ]
        return list_review

    if getenv('HBNB_TYPE_STORAGE') != 'db':
        @property
        def amenities(self):
            """Attribute that returns a list of Amenity instances"""
            values_amenity = models.storage.all("Amenity").values()
            list_amenity = [
                amenity
                for amenity in values_amenity
                if amenity.place_id == self.id
            ]
            return list_amenity
