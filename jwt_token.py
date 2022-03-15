# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 17:21:16 2022

@author: Admin
"""
from flask import Flask, request, jsonify
from models.user import User
from functools import wraps
import jwt
from config import SECRET_KEY

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'message': 'a valid token is missing'})
        
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            # current_user = User.query.filter_by(id=data['id']).first()
            current_user = data['id']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except:
            return jsonify({'message': 'token is invalid'})

        return f(current_user, *args, **kwargs)
    return decorator