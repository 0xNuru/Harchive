#!/usr/bin/python3

"""
This is the base_model inherited by all classes
contains:
    - instances:
        - save 
        - delete 
        - to_dict
        - __repr__ 
        - __str__ 
    - attributes:
        - id attribute
        - created_at attribute
        - updated_at attribute
"""

import uuid
from sqlalchemy import Column, Integer, String, DateTime, VARCHAR
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
import sys
sys.path.insert(0, '..')



# declaring the declarative base

Base = declarative_base()

class BaseModel:
    """
        This class defines all common attributes/methods
        for other class that would inherit it.
    """

    id = Column(String(200), unique=True, nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=(datetime.utcnow()))
    updated_at = Column(DateTime, nullable=False, default=(datetime.utcnow()))

    def __init__(self, *args, **kwargs):
        """
            Initialization of base model class

            Args:
                args: Not used
                Kwargs: constructor for the basemodel

            Attributes:
                id: unique id generated
                created_at: creation date
                updated_at: updated date
        """

        # check if parameters were passed while inheriting
        # and assign the to the base class

        if kwargs:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != "__class__":
                    setattr(self, key, value)
                if "id" not in kwargs:
                    self.id = str(uuid.uuid4())
                if "created_at" not in kwargs:
                    self.created_at = datetime.now()
                if "updated_at" not in kwargs:
                    self.updated_at = datetime.now()

        else:
            self.id = str(uuid.uuid4())
            self.updated_at = self.created_at = datetime.now()

    def __str__(self):
        """
            This instance defines the property of the class in a string fmt
            Return:
                returns a string containing of class name, id and dict
        """
        return f"[{type(self).__name__}] ({self.id}) {self.__dict__}"

    def __repr__(self):
        """
            Return:
                returns a string representation of the calss

        """
        return self.__str__()

    def save(self):
        """
            This instance saves the current attributes in the class
            and updates the updated_at attribute

            Return:
                None
        """
        self.updated_at = datetime.now()

    def to_dict(self):
        """
            This instance creates a dictionary representation of the classs

            Return:
                returns a dict rep of the class containing the
        """

        base_dict = dict(self.__dict__)
        base_dict['__class__'] = str(type(self).__name__)
        base_dict['created_at'] = self.created_at.isoformat()
        base_dict['updated_at'] = self.updated_at.isoformat()

        return base_dict

    # def delete(self):
    #     """
    #         This instance deletes the class
    #         Returns:
    #             None
    #     """
    #     storage.delete(self)
