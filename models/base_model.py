#!/usr/bin/python3
"""Defines the BaseModel class."""
from datetime import datetime
import models
import uuid
from os import getenv
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

# Define the Base class based on the storage type
Base = declarative_base()


class BaseModel:
    """The BaseModel class from which future classes will be derived"""

    if getenv("HBNB_TYPE_STORAGE") == 'db':
        __tablename__ = 'base_model'
        id = Column(String(60), nullable=False, primary_key=True)
        created_at = Column(DateTime, nullable=False,
                            default=datetime.utcnow)
        updated_at = Column(DateTime, nullable=False,
                            default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialize the base model"""
        self.id = str(uuid.uuid4())
        self.created_at = self.updated_at = datetime.now()

        # Update attributes if keyword arguments are provided
        if kwargs:
            for key, value in kwargs.items():
                if key == '__class__':
                    continue
                setattr(self, key, value)

                # Convert date strings to datetime objects
                if key in ['created_at', 'updated_at']:
                    # Define the time format for date parsing
                    time_fmt = "%Y-%m-%dT%H:%M:%S.%f"
                    setattr(self, key, datetime.strptime(value, time_fmt))

    def __str__(self):
        """String representation of the BaseModel class"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)

    def save(self):
        """
        Update the 'updated_at' attribute with
        the current datetime and save to storage
        """
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self, save_to_disk=False):
        """Return a dictionary containing all keys/values of the instance"""
        new_dict = self.__dict__.copy()
        new_dict["__class__"] = self.__class__.__name__
        new_dict.pop('_sa_instance_state', None)

        # Convert datetimes to ISO format strings
        for key in ['created_at', 'updated_at']:
            if key in new_dict:
                new_dict[key] = new_dict[key].isoformat()

        # Rename '_password' to 'password' for serialization
        if '_password' in new_dict:
            new_dict['password'] = new_dict['_password']
            new_dict.pop('_password', None)

        # Remove unnecessary attributes
        for key in ['amenities', 'reviews']:
            new_dict.pop(key, None)

        # Remove 'password' attribute if not saving to disk
        if not save_to_disk:
            new_dict.pop('password', None)

        return new_dict

    def delete(self):
        """Delete the current instance from storage"""
        models.storage.delete(self)
