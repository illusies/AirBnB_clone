#!/usr/bin/python3
"""The implementation of the BaseModel program"""

from uuid import uuid4
from datetime import datetime

class BaseModel:
    """ A class that defines the attributes for all modules"""

    def __init__(self, *args, **kwargs):
        """A function that initializes the BaseModel class attributes
                    
            PARAMETERS
            self: the constructor variable
            *args: a tuple that contains all arguments
            **kwargs: a dictionary that contains all arguments by key/value
        """

        from models import storage
        if not kwargs:
            self.id = str(uuid4())
            self.created_at = self.updated_at = datetime.now()
            storage.new(self)
        else:
            for key, value in kwargs.items():
                if key != '__class__':
                    if key in ('created_at', 'updated_at'):
                        setattr(self, key, datetime.fromisoformat(value))
                    else:
                        setattr(self, key, value)

    def __str__(self):
        """A function that returns the string representation of the object
                    
            PARAMETERS
            self: the constructor variable
        """
        return "[{}] ({}) {}".format(type(self).__name__, self.id,
                                     self.__dict__)

    def save(self):
        """A function that updates 'self.updated_at' with the current datetime
                            
            PARAMETERS
            self: the constructor variable
        """
        
        from models import storage
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """A function that returns a dictionary containing all keys/values of __dict__
                            
            PARAMETERS
            self: the constructor variable
        """
        
        dict_1 = self.__dict__.copy()
        dict_1["__class__"] = self.__class__.__name__
        for k, v in self.__dict__.items():
            if k in ("created_at", "updated_at"):
                v = self.__dict__[k].isoformat()
                dict_1[k] = v
        return dict_1
