#!/usr/bin/python3
"""
This module defines the DBStorage class for database storage using SQLAlchemy.
"""

from os import getenv
from models.base_model import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


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
        user = getenv('HBNB_MYSQL_USER')
        passwd = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        database = getenv('HBNB_MYSQL_DB')

        # Create the SQLAlchemy engine
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(
                user,
                passwd,
                host,
                database
            ),
            pool_pre_ping=True
        )

        # Drop tables if environment is test
        if getenv('HBNB_ENV') == 'test':
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
        if isinstance(cls, str):
            cls = self.classes().get(cls, None)

        if cls:
            # Retrieve objects of a specific class
            for obj in self.__session.query(cls):
                objects[obj.__class__.__name__ + '.' + obj.id] = obj
        else:
            # Retrieve objects of all classes
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

        classes = {
            "BaseModel": BaseModel,
            "User": User,
            "State": State,
            "City": City,
            "Amenity": Amenity,
            "Place": Place,
            "Review": Review
        }
        return classes

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
        """
        Dispose of the current session if active.
        """
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
        if (
            cls is not None
            and isinstance(cls, str)
            and id is not None
            and isinstance(id, str)
            and cls in self.classes()
        ):
            cls = self.classes()[cls]
            result = self.__session.query(cls).filter(cls.id == id).first()
            return result
        else:
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
        total = 0
        if cls is None:
            for cls_name in self.classes().keys():
                total += self.__session.query(self.classes()[cls_name]).count()
        elif isinstance(cls, str) and cls in self.classes():
            cls = self.classes()[cls]
            total = self.__session.query(cls).count()
        return total
