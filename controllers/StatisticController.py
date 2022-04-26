# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 14:44:55 2022

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
from config import SECRET_KEY, UPLOAD_FOLDER
import jwt
import datetime
from werkzeug.exceptions import HTTPException, BadRequest, Unauthorized, Forbidden
from utils.validation import validateEmpty, validateMissingJsonField, validateTimestamp

@token_required
@api_call
def createStatistic(token, cameraId):
    if (token.userRole == 1):
        # id = db.Column(db.Integer, primary_key=True)
        # camera_id = db.Column(db.Integer, db.ForeignKey('cameras.id'))
        # timestamp = db.Column(db.DateTime(timezone=True), nullable=False)
        # crowd_count = db.Column(db.Integer, nullable=False)
        data = request.get_json()
        missingList, isMissing = validateMissingJsonField(data, ['timestamp', 'crowdCount'])
        if (isMissing):
            raise BadRequest([field+" is not provided" for field in missingList])
        emptyFields = validateEmpty(timestamp=data['timestamp'], crowdCount=data['crowdCount'])
        if len(emptyFields) > 0:
            raise BadRequest([field+" is empty" for field in emptyFields])
        validateTimestamp(data['timestamp'])
        new_statistic = Statistic(cameraId, data['timestamp'], data['crowdCount'])
        db.session.add(new_statistic)
        db.session.commit()
        return new_statistic.serialize()
    else:
        raise Forbidden(description = "You Are Not Allowed To Create Camera")

@token_required
@api_call
def getStatisticByTimestamp(token, cameraId):
    camera = Camera.query.filter_by(id=cameraId).first()
    if not camera.is_public:
        camera = CameraOwner.query.filter_by(camera_id=cameraId).first()
        if camera.user_id != token.userId:
            raise Forbidden(description = "You Are Not Allowed To Access Statictic")
    data = request.get_json()
    missingList, isMissing = validateMissingJsonField(data, ['start', 'end'])
    if (isMissing):
        raise BadRequest([field+" is not provided" for field in missingList])
    validateTimestamp(data['start'])
    validateTimestamp(data['end'])
    rows = Statistic.query\
        .filter(Statistic.timestamp >= data['start'], Statistic.timestamp <= data['end'])\
        .order_by(Statistic.timestamp.asc())\
        .all()
    # order_by(Statistic.timestamp.desc()) for desc
    return [s.serialize(exclude=['id', 'cameraId']) for s in rows]