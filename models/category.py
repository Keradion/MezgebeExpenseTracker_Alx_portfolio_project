#!/usr/bin/python3
"""This module holds definition of class Category"""
import os
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

class Category(BaseModel, Base):
    """This class defines a Category by various attributes"""
    __tablename__ = 'categories'
    name = Column(String(128), nullable=True)
    category_description = Column(String(128), nullable=False)


