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

def index():
    # raise BadRequest("error1")
    # raise BadRequest(["error1", "error2"])
    return jsonify([e.serialize() for e in User.query.all()])
def store():
    db.session.add(User(name="mujir", age="24", address="pasuruan"))
    db.session.commit()
    return "user"

@token_required
def show(user):
    return jsonify(User.query.filter_by(id=user.id).first().serialize())

def update(userId):
    return "user"

def delete(userId):
    return "user"

@api_call
def register():  
    data = request.get_json()  
    hashed_password = generate_password_hash(data['password'], method='sha256')
 
    new_user = User(name=data['name'], email=data['email'], password=hashed_password, role=2, picture=None) 
    db.session.add(new_user)  
    db.session.commit()    

    return new_user.serializeWithoutIdAndRole()

def login():
    auth = request.get_json() 

    if not auth or not auth['username'] or not auth['password']:  
        return make_response('could not verify', 401, {'Authentication': 'login required"'})    

    user = User.query.filter_by(name=auth['username']).first()   
     
    if check_password_hash(user.password, auth['password']):

        token = jwt.encode({'id' : user, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=45)}, SECRET_KEY, "HS256")
        return jsonify({'token' : token}) 

    return make_response('could not verify',  401, {'Authentication': '"login required"'})
    return "user"