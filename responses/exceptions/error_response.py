# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 15:56:56 2022

@author: Admin
"""

from flask import jsonify
from functools import wraps

def error_response(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        
        code, status, errors = f(args)
        return jsonify({"code": code, "status": status, "data": None, "errors": errors}), code
        
    return decorator