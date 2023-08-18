#!/usr/bin/python3
"""
This module defines the DBStorage class for database storage using SQLAlchemy.
"""

import os
from models.base_model import Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.review import Review
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


# Mapping of class names to their corresponding classes
class_mapping = {
    'Amenity': Amenity,
    'City': City,
    'Place': Place,
    'State': State,
    'Review': Review,
    'User': User
}


class DBStorage:
    """
    A class for managing database storage using SQLAlchemy.
    """
    __engine = None
    __session = None

    def __init__(self):
        """
        Initialize the DBStorage instance.
        Creates the database engine and manages the session.
        """
        # Get MySQL connection details from environment variables
        user = os.getenv('HBNB_MYSQL_USER')
        passwd = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        database = os.getenv('HBNB_MYSQL_DB')

        # Create the SQLAlchemy engine
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, passwd, host, database))

        # Drop tables if environment is test
        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Retrieve objects from the database.

        Args:
            cls (class): The class of objects to retrieve.
            If None, retrieve all types.

        Returns:
            dict: A dictionary of objects in format {'class_name.id': object}.
        """
        if not self.__session:
            self.reload()

        objects = {}
        if type(cls) == str:
            cls = class_mapping.get(cls, None)

        if cls:
            # Retrieve objects of a specific class
            for obj in self.__session.query(cls):
                objects[obj.__class__.__name__ + '.' + obj.id] = obj
        else:
            # Retrieve objects of all classes
            for cls in class_mapping.values():
                for obj in self.__session.query(cls):
                    objects[obj.__class__.__name__ + '.' + obj.id] = obj

        return objects

    def reload(self):
        """
        Create all tables in the database and initialize a new session.
        """
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def new(self, obj):
        """
        Add a new object to the current database session.

        Args:
            obj: The object to add to the session.
        """
        self.__session.add(obj)

    def save(self):
        """
        Commit all changes of the current database session.
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Delete an object from the current database session.

        Args:
            obj: The object to delete from the session.
        """
        if not self.__session:
            self.reload()
        if obj:
            self.__session.delete(obj)

    def close(self):
        """Dispose of current session if active"""
        self.__session.remove()

    def get(self, cls, id):
        """Retrieve an object"""
        if cls is not None and type(cls) is str and id is not None and\
           type(id) is str and cls in class_mapping:
            cls = class_mapping[cls]
            result = self.__session.query(cls).filter(cls.id == id).first()
            return result
        else:
            return None

    def count(self, cls=None):
        """Count number of objects in storage"""
        total = 0
        if type(cls) == str and cls in class_mapping:
            cls = class_mapping[cls]
            total = self.__session.query(cls).count()
        elif cls is None:
            for cls in class_mapping.values():
                total += self.__session.query(cls).count()
        return total
