# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 11:29:37 2022

@author: Admin
"""

from database import Database

db = Database().db

class Statistic(db.Model):
    __tablename__ = 'statistics'
    id = db.Column(db.Integer, primary_key=True)
    camera_id = db.Column(db.Integer, db.ForeignKey('cameras.id'))
    timestamp = db.Column(db.DateTime(timezone=True), nullable=False)
    # Fri, 15 Apr 2022 22:00:00 GMT
    crowd_count = db.Column(db.Integer, nullable=False)
    
    def __init__(self, camera_id, timestamp, crowd_count):
        self.camera_id = camera_id
        self.timestamp = timestamp
        self.crowd_count = crowd_count
        
    def __repr__(self):
        return '<Statisctic %r>' % self.camera_id
    
    def serialize(self, exclude = None):
        response = {
            'id': self.id,
            'cameraId': self.camera_id,
            'timestamp': self.timestamp,
            'crowdCount': self.crowd_count
        }
        if (isinstance(exclude, list)):
            for key in exclude:
                del response[key]
        return response