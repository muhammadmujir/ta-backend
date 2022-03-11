# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 16:57:57 2022

@author: Admin
"""

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]