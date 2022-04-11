# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 10:56:59 2022

@author: Admin
"""

from database import Database
from sqlalchemy.orm import relationship

db = Database().db

class Camera(db.Model):
    __tablename__ = 'cameras'
    id = db.Column(db.Integer, primary_key=True)
    rtsp_address = db.Column(db.String, unique=True, nullable=False)
    location = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    area = db.Column(db.Float(precision=2), nullable=False)
    max_crowd_count = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)
    is_public = db.Column(db.Boolean, nullable=False)
    picture = db.Column(db.String, nullable=True)
    camera_owners = relationship("CameraOwner")
    statistics = relationship("Statistic")
    
    def __init__(self, rtsp_address, location, description, area, max_crowd_count, is_active, is_public, picture):
        self.rtsp_address = rtsp_address
        self.location = location
        self.description = description
        self.area = area
        self.max_crowd_count = max_crowd_count
        self.is_active = is_active
        self.is_public = is_public
        self.picture = picture
        
    def __repr__(self):
        return '<Camera %r>' % self.rtsp_address
    
    def serialize(self, exclude = None):
        response = {
            'id': self.id,
            'rtspAddress': self.rtsp_address,
            'location': self.location,
            'description': self.description,
            'area': self.area,
            'maxCrowdCount': self.max_crowd_count,
            'isActive': self.is_active,
            'isPublic': self.is_public,
            'picture': self.picture
        }
        if (isinstance(exclude, list)):
            for key in exclude:
                del response[key]
        return response