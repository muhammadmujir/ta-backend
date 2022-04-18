# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 09:39:00 2022

@author: Admin
"""
import re
from datetime import datetime
from werkzeug.exceptions import BadRequest

def validateTimestamp(dateStr):
    try:
        # correct timestamp -> 1999-12-23 00:19:00+0700
        # +0700 -> timezone WIB
        datetime.strptime(dateStr, '%Y-%m-%d %H:%M:%S%z')
    except ValueError:
        raise BadRequest("Wrong timestamp format")
        
def validateMissingJsonField(json, keys):
    missingList = []
    for key in keys:
        if not key in json:
            missingList.append(key)
    return missingList, len(missingList) > 0

def validateEmpty(**data):
    emptyList = []
    for key, value in data.items():
        if (isinstance(value, str) and value == ""):
            emptyList.append(key)
    return emptyList

def validateEmail(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.fullmatch(regex, email)