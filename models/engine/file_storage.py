#!/usr/bin/python3
"""This module defines a class FileStorage"""

import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

class FileStorage:
    """Serializes instances to a JSON file & deserializes back to instances"""

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage.
        If cls is provided, only return objects of that class."""
        if cls is not None:
            return {
                key: obj
                for key, obj in self.__objects.items()
                if isinstance(obj, cls)
            }
        return self.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        """Saves storage dictionary to file"""
        with open(self.__file_path, 'w') as f:
            json.dump({
                key: obj.to_dict()
                for key, obj in self.__objects.items()
            }, f)

    def reload(self):
        """Loads storage dictionary from file"""
        try:
            with open(self.__file_path, 'r') as f:
                objs = json.load(f)
                for key, val in objs.items():
                    cls_name = val["__class__"]
                    self.__objects[key] = eval(cls_name)(**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Deletes obj from __objects if it exists"""
        if obj is None:
            return
        key = f"{obj.__class__.__name__}.{obj.id}"
        if key in self.__objects:
            del self.__objects[key]
            self.save()
