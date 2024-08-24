#!/usr/bin/python3
"""This module holds definition of class Expense"""
import os
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

class Expense(BaseModel, Base):
    """This class defines an Expense by various attributes"""
    __tablename__ = 'expenses'
    expense_amount = Column(Integer, nullable=True)
    expense_description = Column(String(128), nullable=False)


