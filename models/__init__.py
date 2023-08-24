#!/usr/bin/python3
"""
This module instantiates an object of class FileStorage or DBStorage
based on the environment variable.
"""
from os import getenv


if getenv('HBNB_storage_type') == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
# Reload the storage to load data from the storage backend
storage.reload()
