# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 23:29:55 2022

@author: Admin
"""

import os
import glob
from flask import send_from_directory
from datetime import datetime

def getFileExtension(path, uniqueName):
    filenames = glob.glob(os.path.join(path, str(uniqueName)+".*"))
    if len(filenames) == 0:
        return None
    return filenames[0].rsplit('.', 1)[1]

def getPicture(path, uniqueName):
    ext =  getFileExtension(uniqueName)
    return send_from_directory(path, str(uniqueName)+"."+ext)    

def allowedFile(filename, allowedExtendions = { 'png', 'jpg', 'jpeg' }):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowedExtendions

def removeExistingFile(path, itemId):
    ext = getFileExtension(path, itemId)
    if ext != None:
        os.remove(os.path.join(path, str(itemId)+"."+ext))
        
def getStrDateFromTimestamp(timeInMillis):
    dateTime = datetime.fromtimestamp(timeInMillis)
    return dateTime.strftime('%Y-%m-%d %H:%M:%S%z')

def getCurrentStrDate():
    return getStrDateFromTimestamp(datetime.timestamp(datetime.now()))    