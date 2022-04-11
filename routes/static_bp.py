# -*- coding: utf-8 -*-
"""
Created on Sun Apr 10 21:42:24 2022

@author: Admin
"""

from flask import Blueprint
from controllers.CameraController import *
from utils.constant import BASE_URL

static_bp = Blueprint('static_bp', __name__, url_prefix=BASE_URL+"/static/images")
static_bp.route('/cameras/<cameraId>', methods=['GET'])(getCameraPicture)
static_bp.route('/cameras/<cameraId>', methods=['PUT'])(uploadCameraPicture)