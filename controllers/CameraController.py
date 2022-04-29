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
from models.statistic import Statistic
from jwt_token import token_required
from responses.api_call import api_call
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from config import SECRET_KEY, UPLOAD_FOLDER_CAMERA, SQLALCHEMY_DATABASE_URI
import jwt
import datetime
from werkzeug.exceptions import HTTPException, BadRequest, Unauthorized, Forbidden
from utils.validation import validateEmpty, validateEmail, validateMissingJsonField
from utils.util import getCurrentStrDate
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
import random
from torchvision import datasets, transforms
from crowd_counting.inceptionresnetv2 import InceptionResNetV2
import cv2
import torch
import time
import PIL.Image as Image
import numpy as np
from datetime import datetime
import functools
from application import Application
from crowd_counting.crowd_counting import *
from utils.util import *

app = Application().app
scheduler = Application().scheduler

def crowdCounting(cameraId):
    with app.app_context():
        camera = cv2.VideoCapture(Camera.query.filter_by(id=cameraId).first().rtsp_address)
        # camera = cv2.VideoCapture("C:\\Users\\Admin\\Downloads\\videoplayback (1).mp4")
        crowd = 0
        iteration = 5
        for i in range(iteration):
            success, frame = camera.read()
            if not success:
                break
            else:
                im = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                im = Image.fromarray(np.uint8(np.array(im)))
                im = transform(im).cpu()
                # im.save("C:\\Users\\Admin\\Desktop\\TA\\Dataset\\UCF-QNRF_ECCV18\\Test\\debug\\coba.jpg")
                # calculate crowd count
                output = model(im.unsqueeze(0))
                crowd = crowd + output.detach().cpu().sum().numpy()
                if i == iteration-1:
                    crowd = crowd / iteration
                    new_statistic = Statistic(cameraId, getCurrentStrDate(), crowd)
                    db.session.add(new_statistic)
                    db.session.commit()
        
def schedule(cameraId, isAddJob = True):
    cameraId = str(cameraId)
    # scheduler.start()
    if isAddJob:
        if scheduler.get_job(cameraId) == None:
            minute = int(random.random() * 59)
            scheduler.add_job(crowdCounting, 'cron', hour='6-23', minute=5, id=cameraId, args=[cameraId])
    else:
        if scheduler.get_job(cameraId):
            scheduler.remove_job(cameraId)
    scheduler.print_jobs()
    
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
        if data['isActive']:
            schedule(new_camera.id, True)
        return new_camera.serialize()
    else:
        raise Forbidden(description = "You Are Not Allowed To Create Camera")

@token_required
@api_call
def updateCamera(token, cameraId):
    if (token.userRole == 1):
        if CameraOwner.query.filter_by(user_id=token.userId).filter_by(camera_id=cameraId).first() == None:
            raise Forbidden(description = "You Are Not Allowed To Edit Camera")
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
        if data['isActive']:
            schedule(camera.id, True)
        else:
            schedule(camera.id, False)
        return camera.serialize()
    else:
        raise Forbidden(description = "You Are Not Allowed To Edit Camera")

@token_required
@api_call
def deleteCamera(token, cameraId):
    if (token.userRole == 1):
        if CameraOwner.query.filter_by(user_id=token.userId).filter_by(camera_id=cameraId).first() == None:
            raise Forbidden(description = "You Are Not Allowed To Delete Camera")
        deletedRows = Camera.query.filter_by(id=cameraId).delete()
        if deletedRows > 0:
            db.session.commit()
            ext = getFileExtension(cameraId)
            if ext != None:
                os.remove(os.path.join(UPLOAD_FOLDER_CAMERA, cameraId+"."+ext))
            schedule(cameraId, False)
        else:
            raise BadRequest("Camera Not Found")
        return None
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
            removeExistingFile(UPLOAD_FOLDER_CAMERA, cameraId)
            filename = str(cameraId)+"."+file.filename.rsplit('.', 1)[1]
            # filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER_CAMERA, filename))
            # return str(os.path.join(UPLOAD_FOLDER_CAMERA, filename))
            return "Upload Success"
        raise BadRequest("File Extension Not Supported")
    else:
        raise Forbidden(description = "You Are Not Allowed To Edit Camera")


def getFileExtension(cameraId):
    filenames = glob.glob(os.path.join(UPLOAD_FOLDER_CAMERA, str(cameraId)+".*"))
    if len(filenames) == 0:
        return None
    return filenames[0].rsplit('.', 1)[1]

def getCameraPicture(cameraId):
    ext =  getFileExtension(cameraId)
    return send_from_directory(UPLOAD_FOLDER_CAMERA, str(cameraId)+"."+ext)    

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

@token_required
@api_call
def getAllCameraList(token):
    if token.userRole == 1:
        return [row.serialize() for row in Camera.query.all()]
    else:
        return [c.serialize(exclude=['isActive', 'isPublic']) for c in Camera.query.filter(Camera.is_active == True, Camera.is_public == True).all()]

@token_required
@api_call
def getCameraDetail(token, cameraId):
    camera = Camera.query.filter_by(id=cameraId).first()
    if camera == None:
        raise BadRequest("Camera Not Found")
    if not camera.is_public:
        if not CameraOwner.query.filter_by(camera_id=cameraId, user_id=token.userId).first():
            raise Forbidden(description = "You Are Not Allowed To Access Camera")
    return camera.serialize()