# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 09:39:00 2022

@author: Admin
"""
import re

def validateEmpty(**data):
    emptyList = []
    for key, value in data.items():
        if (isinstance(value, str) and value == ""):
            emptyList.append(key)
    return emptyList

def validateEmail(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.fullmatch(regex, email)