# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 21:52:26 2022

@author: Admin
"""

from flask import Blueprint
from controllers.CameraController import *
from utils.constant import BASE_URL

camera_bp = Blueprint('camera_bp', __name__, url_prefix=BASE_URL+"/cameras")
camera_bp.route('', methods=['GET'])(getOwnerCameraList)
camera_bp.route('/_all', methods=['GET'])(getAllCameraList)
camera_bp.route('/_publicCamera', methods=['GET'])(getPublicCameraList)
camera_bp.route('', methods=['POST'])(createCamera)
camera_bp.route('/<cameraId>', methods=['GET'])(getCameraDetail)
camera_bp.route('/<cameraId>', methods=['PUT'])(updateCamera)
camera_bp.route('/<cameraId>', methods=['DELETE'])(deleteCamera)