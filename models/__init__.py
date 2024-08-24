#!/usr/bin/python3
""" Determine storage 
"""
from models.engine.db_storage import DBStorage

storage = DBStorage()
storage.reload()
