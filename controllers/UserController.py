# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 21:01:08 2022

@author: Admin
"""

import sys
from flask import render_template, redirect, url_for, request, abort, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from models.user import User, db
from jwt_token import token_required
from responses.api_call import api_call
from werkzeug.security import generate_password_hash, check_password_hash
from config import SECRET_KEY
import jwt
import datetime
from werkzeug.exceptions import HTTPException, BadRequest, Unauthorized
from utils.validation import validateEmpty, validateEmail

def index():
    # raise BadRequest("error1")
    # raise BadRequest(["error1", "error2"])
    return jsonify([e.serialize() for e in User.query.all()])
def store():
    db.session.add(User(name="mujir", age="24", address="pasuruan"))
    db.session.commit()
    return "user"

@token_required
@api_call
def show(userId):
    return User.query.filter_by(id=userId).first().serialize()

def update(userId):
    return "user"

def delete(userId):
    return "user"

@api_call
def register():  
    data = request.get_json() 
    emptyFields = validateEmpty(name=data['name'], email=data['email'], password=data['password'])
    if len(emptyFields) > 0:
        raise BadRequest([field+" is empty" for field in emptyFields])
    if not validateEmail(data['email']):
        raise BadRequest("Wrong email format")
    emailExist = User.query.filter_by(email=data['email']).first()
    if (emailExist is not None):
        raise BadRequest("user already exists")
    hashed_password = generate_password_hash(data['password'], method='sha256')
 
    new_user = User(name=data['name'], email=data['email'], password=hashed_password, role=2, picture=None) 
    db.session.add(new_user)  
    db.session.commit()    

    return new_user.serializeWithoutIdAndRole()

@api_call
def login():
    auth = request.get_json() 

    if not auth or not auth['email'] or not auth['password']: 
        raise Unauthorized("email and password are empty")

    user = User.query.filter_by(email=auth['email']).first()   
    if user is None:
        raise Unauthorized("email has not registered yet")
    if check_password_hash(user.password, auth['password']):
        token = jwt.encode({'id' : user.id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(days=2)}, SECRET_KEY, "HS256")
        return {'token' : token}
    else :
        raise Unauthorized("wrong password")