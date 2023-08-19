#!/usr/bin/python3
"""
ALX HolbertonBnB - File and Database Storage

This module defines the FileStorage class, which handles
the serialization and deserialization of objects to/from JSON format.
It manages the storage of objects both in a file-based database and
in a database managed by SQLAlchemy.

Attributes:
    __file_path (str): The path to the JSON file where objects are stored.
    __objects (dict): A dictionary containing all loaded objects,
    with their class name and ID as keys.
"""

import datetime
import json
import os


class FileStorage:
    """
    The FileStorage class handles the serialization and
    deserialization of objects to/from JSON format and also manages objects
    in a database.

    Attributes:
        __file_path (str): The path to the JSON file where objects are stored.
        __objects (dict): A dictionary containing all loaded objects,
        with their class name and ID as keys.
    """

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """
        Retrieves all objects or objects of a specific class.

        Args:
            cls (class): The class of objects to retrieve.
            If None, retrieves all objects.

        Returns:
            dict: A dictionary containing the retrieved objects.
        """
        if not cls:
            return self.__objects
        elif isinstance(cls, str):
            return {k: v for k, v in self.__objects.items()
                    if v.__class__.__name__ == cls}
        else:
            return {k: v for k, v in self.__objects.items()
                    if isinstance(v, cls)}

    def new(self, obj):
        """
        Adds a new object to the storage.

        Args:
            obj: The object to add.
        """
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects[key] = obj

    def save(self):
        """
        Serializes __objects to JSON file.
        """
        json_objects = {}
        for key in self.__objects:
            json_objects[key] = self.__objects[key].to_dict(save_to_disk=True)
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """
        Deserializes JSON file into __objects.
        """
        if not os.path.isfile(self.__file_path):
            return

        with open(self.__file_path, "r", encoding="utf-8") as f:
            obj_dict = json.load(f)
            obj_dict = {k: self.classes()[v["__class__"]](**v)
                        for k, v in obj_dict.items()}
            self.__objects = obj_dict

            # Update missing objects in the storage
            for obj in self.__objects.values():
                obj_class = type(obj).__name__
                obj_id = obj.id
                obj_key = "{}.{}".format(obj_class, obj_id)
                if obj_key not in self.__objects:
                    self.__objects[obj_key] = obj

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

    def get(self, cls, id):
        """
        Retrieves an object by class and ID.

        Args:
            cls (class): The class of the object.
            id (str): The ID of the object.

        Returns:
            object: The retrieved object.
        """
        if isinstance(cls, str) and cls in self.classes:
            key = cls + '.' + id
            return self.__objects.get(key, None)
        return None

    def delete(self, obj=None):
        """
        Deletes the given object from __objects.

        Args:
            obj: The object to delete.
        """
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            self.__objects.pop(key, None)
            self.save()

    def close(self):
        """
        Closes the database session.
        """
        self.reload()

    def count(self, cls=None):
        """Count number of objects in storage"""
        count = 0
        if type(cls) == str and cls in self.classes:
            count = len(self.all(cls))
        elif cls is None:
            count = len(self.__objects)
        return count
