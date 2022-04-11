# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 21:01:08 2022

@author: Admin
"""

import sys
import os
import glob
from flask import render_template, redirect, url_for, request, abort, jsonify, make_response, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from models.user import User, db
from models.camera import Camera
from models.camera_owner import CameraOwner
from jwt_token import token_required
from responses.api_call import api_call
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from config import SECRET_KEY, UPLOAD_FOLDER
import jwt
import datetime
from werkzeug.exceptions import HTTPException, BadRequest, Unauthorized, Forbidden
from utils.validation import validateEmpty, validateEmail, validateMissingJsonField

@token_required
@api_call
def createCamera(token):
    if (token.userRole == 1):
        # rtsp_address = db.Column(db.String, unique=True, nullable=False)
        # location = db.Column(db.String, nullable=False)
        # description = db.Column(db.String, nullable=True)
        # area = db.Column(db.Float(precision=2), nullable=False)
        # max_crowd_count = db.Column(db.Integer, nullable=False)
        # is_active = db.Column(db.Boolean, nullable=False)
        # is_public = db.Column(db.Boolean, nullable=False)
        # picture = db.Column(db.String, nullable=True)
        # camera_owners = relationship("CameraOwner")
        # statistics = relationship("Statistic")
        data = request.get_json()
        missingList, isMissing = validateMissingJsonField(data, ['rtspAddress', 'location', 'area', 'maxCrowdCount', 'isActive', 'isPublic'])
        if (isMissing):
            raise BadRequest([field+" is not provided" for field in missingList])
        emptyFields = validateEmpty(rtspAddress=data['rtspAddress'], location=data['location'], area=data['area'], maxCrowdCount=data['maxCrowdCount'], 
                                    isActive=data['isActive'], isPublic=data['isPublic'])
        if len(emptyFields) > 0:
            raise BadRequest([field+" is empty" for field in emptyFields])
        description = data['description'] if 'description' in data else None
        new_camera = Camera(data['rtspAddress'], data['location'], description, data['area'], data['maxCrowdCount'], data['isActive'], data['isPublic'], None)
        db.session.add(new_camera) 
        # flush will basically communicate your changes to db in a pending state.
        # commit will actually write them into db
        db.session.flush()
        new_camera_owner = CameraOwner(new_camera.id, token.userId)
        db.session.add(new_camera_owner)
        db.session.commit()
        return new_camera.serialize()
    else:
        raise Forbidden(description = "You Are Not Allowed To Create Camera")

@token_required
@api_call
def updateCamera(token, cameraId):
    if (token.userRole == 1):
        data = request.get_json()
        missingList, isMissing = validateMissingJsonField(data, ['rtspAddress', 'location', 'area', 'maxCrowdCount', 'isActive', 'isPublic'])
        if (isMissing):
            raise BadRequest([field+" is not provided" for field in missingList])
        emptyFields = validateEmpty(rtspAddress=data['rtspAddress'], location=data['location'], area=data['area'], maxCrowdCount=data['maxCrowdCount'], 
                                    isActive=data['isActive'], isPublic=data['isPublic'])
        if len(emptyFields) > 0:
            raise BadRequest([field+" is empty" for field in emptyFields])
        description = data['description'] if 'description' in data else None
        camera = Camera.query.filter_by(id=cameraId).first()
        camera.rtsp_address = data['rtspAddress']
        camera.location = data['location']
        camera.description = description
        camera.area = data['area']
        camera.max_crowd_count = data['maxCrowdCount']
        camera.is_active = data['isActive']
        camera.is_public = data['isPublic']
        db.session.commit()
        return camera.serialize()
    else:
        raise Forbidden(description = "You Are Not Allowed To Edit Camera")

@token_required
@api_call
def deleteCamera(token, cameraId):
    if (token.userRole == 1):
        deletedRows = Camera.query.filter_by(id=cameraId).delete()
        if deletedRows > 0:
            db.session.commit()
            ext = getFileExtension(cameraId)
            if ext != None:
                os.remove(os.path.join(UPLOAD_FOLDER, cameraId+"."+ext))
        else:
            raise BadRequest("Camera Not Found")
        return "Delete Successfull"
    else:
        raise Forbidden(description = "You Are Not Allowed To Delete Camera")
        
def allowedFile(filename):
    allowedExtendions = { 'png', 'jpg', 'jpeg' }
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowedExtendions

@token_required
@api_call
def uploadCameraPicture(token, cameraId):
    if (token.userRole == 1):
        if 'file' not in request.files:
            raise BadRequest("No file part")
        file = request.files['file']
        if file.filename == '':
            raise BadRequest("No selected file")
        if file and allowedFile(file.filename):
            filename = str(cameraId)+"."+file.filename.rsplit('.', 1)[1]
            # filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            # return str(os.path.join(UPLOAD_FOLDER, filename))
            return "Upload Success"
    else:
        raise Forbidden(description = "You Are Not Allowed To Edit Camera")


def getFileExtension(cameraId):
    filenames = glob.glob(os.path.join(UPLOAD_FOLDER, str(cameraId)+".*"))
    if len(filenames) == 0:
        return None
    return filenames[0].rsplit('.', 1)[1]

def getCameraPicture(cameraId):
    ext =  getFileExtension(cameraId)
    return send_from_directory(UPLOAD_FOLDER, str(cameraId)+"."+ext)    

@api_call
def getPublicCameraList():
    return [c.serialize(exclude=['isActive', 'isPublic']) for c in Camera.query.filter(Camera.is_active == True, Camera.is_public == True).all()]

@token_required
@api_call
def getOwnerCameraList(token):
    active = request.args.get('active')
    public = request.args.get('public')
    query = Camera.query\
        .join(CameraOwner, Camera.id == CameraOwner.camera_id)
    if (active != None):
        active = active.lower().strip()
        if (active == 'true'):
            query = query.filter(Camera.is_active == True)
        else:
            query = query.filter(Camera.is_active == False)
    if (public != None):
        public = public.lower().strip()
        if (public == 'true'):
            query = query.filter(Camera.is_public == True)
        else:
            query = query.filter(Camera.is_public == False)
    return [row.serialize() for row in query.all()]

def getCameraDetail():
    return "camera"