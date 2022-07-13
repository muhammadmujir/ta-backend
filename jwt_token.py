# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 17:21:16 2022

@author: Admin
"""
from flask import request
from functools import wraps
from werkzeug.exceptions import Unauthorized
import jwt
from config import SECRET_KEY

class TokenContent():
    def __init__(self, userId, userRole):
        self.userId = userId
        self.userRole = userRole
        
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            raise Unauthorized("a valid token is missing")
        
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = TokenContent(data['id'], data['role'])
        except jwt.ExpiredSignatureError:
            raise Unauthorized("Token is expired")
        except:
            raise Unauthorized("Token is invalid")

        return f(current_user, *args, **kwargs)
    return decorator