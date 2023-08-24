#!/usr/bin/python3
"""
This module defines the DBStorage class for database storage using SQLAlchemy.
"""

from os import getenv
from models.base_model import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import SQLAlchemyError  # Import for error handling


class DBStorage:
    """
    A class for managing database storage using SQLAlchemy.
    """

    # Private class attributes
    __engine = None
    __session = None

    def __init__(self):
        """
        Initialize the DBStorage instance.
        Creates the database engine and manages the session.
        """
        # Get MySQL connection details from environment variables
        user = getenv('HBNB_MYSQL_USER', default='your_default_user')
        passwd = getenv('HBNB_MYSQL_PWD', default='your_default_password')
        host = getenv('HBNB_MYSQL_HOST', default='localhost')
        database = getenv('HBNB_MYSQL_DB', default='your_default_db')

        # Create the SQLAlchemy engine
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(
                user,
                passwd,
                host,
                database
            ),
            pool_pre_ping=True  # Option specified as required
        )
        self.__session = None  # Initialize the session here

        # Drop tables if the environment is 'test'
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)  # Requirement implemented

    def all(self, cls=None):
        """
        Retrieve objects from the database.

        Args:
            cls (class): The class of objects to retrieve.
                         If None, retrieve all types.

        Returns:
            dict: A dictionary of objects in format {'class_name.id': object}.
        """
        # Query on the current database session (self.__session) all objects
        # depending on the class name (argument cls)
        if cls:
            if isinstance(cls, str):
                cls = self.classes().get(cls)
            result = {}
            for obj in self.__session.query(cls):
                result[f"{obj.__class__.__name__}.{obj.id}"] = obj
            return result
        else:
            objects = {}
            for cls in self.classes().values():
                for obj in self.__session.query(cls):
                    objects[obj.__class__.__name__ + '.' + obj.id] = obj
            return objects

    def classes(self):
        """
        Returns a dictionary of valid classes and their references.
        """
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review
        return {
            "BaseModel": BaseModel,
            "User": User,
            "State": State,
            "City": City,
            "Amenity": Amenity,
            "Place": Place,
            "Review": Review
        }

    def reload(self):
        """
        Reload the database and create a new session.
        """
        if self.__session:
            self.__session.close()  # Close the current session
        factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        # Create all tables in the database
        Base.metadata.create_all(self.__engine)
        # Create the current database session
        self.__session = scoped_session(factory)

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
        try:
            # Commit all changes of the current database session
            self.__session.commit()
        except SQLAlchemyError as e:
            self.__session.rollback()
            print("Error while saving to database:", str(e))  # Error handling

    def delete(self, obj=None):
        """
        Delete an object from the current database session.

        Args:
            obj: The object to delete from the session.
        """
        if obj:
            self.__session.delete(obj)

    def close(self):
        """
        Dispose of the current session if active.
        """
        if self.__session:
            self.__session.close()

    def get(self, cls, id):
        """
        Retrieve an object.

        Args:
            cls (str): The class name of the object.
            id (str): The ID of the object.

        Returns:
            object: The retrieved object, or None if not found.
        """
        if cls and isinstance(cls, str) and cls in self.classes():
            cls = self.classes()[cls]
            return self.__session.query(cls).filter(cls.id == id).first()
        return None

    def count(self, cls=None):
        """
        Count the number of objects in storage.

        Args:
            cls (str, optional): The class name of the objects to count.
                                 If None, count all objects.

        Returns:
            int: The total count of objects.
        """
        if cls:
            if isinstance(cls, str) and cls in self.classes():
                cls = self.classes()[cls]
                return self.__session.query(cls).count()
            return 0
        total = 0
        for cls_name in self.classes().keys():
            total += self.__session.query(self.classes()[cls_name]).count()
        return total
