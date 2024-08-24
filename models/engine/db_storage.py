#!/usr/bin/python3
"""
Contains the class DBStorage
"""

import models
from models.user import User
from models.expense import Expense
from models.category import Category
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {"User": user, "Expense": Expense,
           "Category": Category}


class DBStorage:
    """interaacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(HBNB_MYSQL_USER,
                                             HBNB_MYSQL_PWD,
                                             HBNB_MYSQL_HOST,
                                             HBNB_MYSQL_DB))

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def get(self, cls, id):
        """ Returns the object based on the class and its Id or none 
            if it is not found 
        """
        if cls is None and id is None:
            return None 
        elif cls is not None and id is not None:
            identifier = cls.__name__ + '.' + id
            objects_in_database = self.all(cls)
            for key in objects_in_database.keys():
                if key == identifier:
                    return objects_in_database[key]
        else:
            objects_in_database = self.all()
            return len(objects_in_database)

    def count(self, cls=None):
        """ Return the number of objects in storage matching the
            given class , count of all objects in storage if no
            cls passed
        """
        count = 0
        if cls is None:
            objects_in_database = self.all()
            return len(objects_in_database)
        else:
             objects_in_database = self.all(cls)
             for key in objects_in_database.keys():
                 if cls.__name__ in key:
                     count = count + 1

             return count 
    
    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()
