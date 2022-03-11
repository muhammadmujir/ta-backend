# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 16:44:23 2022

@author: Admin
"""

from singleton import Singleton
from flask_sqlalchemy import SQLAlchemy

class Database(metaclass=Singleton):
    def __init__(self):
        self.db = SQLAlchemy()