# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 20:56:28 2022

@author: Admin
"""

import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))
# Enable debug mode.
DEBUG = True
# Connect to the database
# SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:root@localhost:5432/ta_crowd_counting'
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/ta_crowd_counting'
# Turn off the Flask-SQLAlchemy event system and warning
SQLALCHEMY_TRACK_MODIFICATIONS = False
# disable json keys sorting
JSON_SORT_KEYS = False
# JWT
SECRET_KEY = '004f2af45d3a4e161a7dd2d17fdae47f'
UPLOAD_FOLDER = 'E:\\ta_project\\source\\images\\'
UPLOAD_FOLDER_CAMERA = UPLOAD_FOLDER+"camera"
UPLOAD_FOLDER_USER = UPLOAD_FOLDER+"user"
MAX_CONTENT_LENGTH = 16 * 1024 * 1024 # 16 MB