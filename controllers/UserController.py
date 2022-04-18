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
from config import SECRET_KEY, UPLOAD_FOLDER_USER
import jwt
from datetime import datetime, timedelta
from werkzeug.exceptions import HTTPException, BadRequest, Unauthorized
from utils.validation import validateEmpty, validateEmail
from utils.util import *

def index():
    # raise BadRequest("error1")
    # raise BadRequest(["error1", "error2"])
    # to get query -> request.args.get('key')
    return request.args.get('user_id')
    return jsonify([e.serialize() for e in User.query.all()])

def userDetail(user_id, name):
    if (request.args.get('query')):
        print("masuk pertama")
    else:
        print("masuk kedua")
    return request.args.get('query')
    return user_id
    return request.view_args.get('user_id')


@token_required
@api_call
def show(tokenContent):
    return User.query.filter_by(id=tokenContent.userId).first().serialize()

@token_required
@api_call
def updateUser(token):
    user = User.query.filter_by(id=token.userId).first()
    isUpdated = False
    data = request.get_json()
    if 'name' in data:
        user.name = data['name']
        isUpdated = True
    if 'oldPassword' and 'newPassword' in data:
        if check_password_hash(user.password, data['oldPassword']):
            user.password = generate_password_hash(data['newPassword'], method='sha256')
            isUpdated = True
        else:
            raise BadRequest("Old Password Not Match")
    if isUpdated:
        db.session.commit()
        return user.serialize()
    raise BadRequest("Empty Request Body")

@token_required
@api_call
def uploadUserPicture(token):
    if 'file' not in request.files:
        raise BadRequest("No file part")
    file = request.files['file']
    if file.filename == '':
        raise BadRequest("No selected file")
    if file and allowedFile(file.filename):
        filename = str(token.userId)+"."+file.filename.rsplit('.', 1)[1]
        file.save(os.path.join(UPLOAD_FOLDER_USER, filename))
        return "Upload Success"
    raise BadRequest("File Extension Not Supported")


def getUserPicture(userId):
    ext =  getFileExtension(cameraId)
    return send_from_directory(UPLOAD_FOLDER_USER, str(userId)+"."+ext)    

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
        token = jwt.encode({'id' : user.id, 'role': user.role, 'exp' : datetime.utcnow() + timedelta(days=2)}, SECRET_KEY, "HS256")
        return {'token' : token}
    else :
        raise Unauthorized("wrong password")