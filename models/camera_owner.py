# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 11:16:16 2022

@author: Admin
"""

from database import Database

db = Database().db

class CameraOwner(db.Model):
    __tablename__ = 'camera_owners'
    id = db.Column(db.Integer, primary_key=True)
    camera_id = db.Column(db.Integer, db.ForeignKey('cameras.id', onupdate="CASCADE", ondelete="CASCADE"))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def __init__(self, camera_id, user_id):
        self.camera_id = camera_id
        self.user_id = user_id
        
    def __repr__(self):
        return '<Camera Owner %r>' % self.camera_id
    
    def serialize(self):
        return {
            'id': self.id,
            'cameraId': self.camera_id,
            'userId': self.user_id
        }
