# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 20:57:58 2022

@author: Admin
"""
from sqlalchemy.orm import relationship
from database import Database
from models.camera_owner import CameraOwner

db = Database().db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.SmallInteger, nullable=False)
    picture = db.Column(db.String, nullable=True)
    camera_owners = relationship("CameraOwner")
    
    def __init__(self, name, email, password, role, picture):
        self.name = name
        self.email = email
        self.password = password
        self.role = role
        self.picture = picture
        
    def __repr__(self):
        return '<User %r>' % self.name
    
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'picture': self.picture
        }
    
    def serializeWithoutIdAndRole(self):
        return {
            'name': self.name,
            'email': self.email,
            'picture': self.picture
        }