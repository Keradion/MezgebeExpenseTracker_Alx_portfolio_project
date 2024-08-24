#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import os
import models
import uuid
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()



class BaseModel:
    """A base class for all hbnb models"""
    
    id = Column(String(60), nullable=False, primary_key=True, unique=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.now())

    def __init__(self, *args, **kwargs):
        flag = 1
        # recreate an instance
        for key, value in kwargs.items():
            if key in ('created_at', 'updated_at'):
                setattr(self, key, datetime.fromisoformat(value))
                flag = 0
            elif key != '__class__':
                setattr(self, key, value)
        if flag == 1:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()


    def __str__(self):
        """Returns a string representation of the instance"""
        return ('[{}] ({}) {}'.
                format(self.__class__.__name__, self.id, self.__dict__))

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        import models 
        self.updated_at = datetime.now()
        print(self)
        models.storage.new(self)
        models.storage.save()

    def delete(self):
        """ delete the current instance from storage """
        from models import storage
        storage.delete(self)

    def to_dict(self):
        """Convert instance into dict format"""
        new_dict = {}

        for key, value in self.__dict__.items():
            if key != '_sa_instance_state':
                if (key == 'created_at' or key == 'updated_at'):
                    new_dict[key] = value.isoformat()
                else:
                    new_dict[key] = value

        new_dict['__class__'] = self.__class__.__name__
        return new_dict
