# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 09:25:28 2022

@author: Admin
"""

from flask import jsonify
from functools import wraps

def api_call(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        
        response = f(*args, **kwargs)
        return jsonify({"code": 200, "status": "OK", "data": response, "errors": None}), 200
        
    return decorator