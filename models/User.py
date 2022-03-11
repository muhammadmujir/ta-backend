# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 20:57:58 2022

@author: Admin
"""

from database import Database

db = Database().db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.String(120))
    address = db.Column(db.String(120))
    password = db.Column(db.String(120))
    
    def __init__(self, name, age, address, password):
        self.name = name
        self.age = age
        self.address = address
        self.password = password
        
    def __repr__(self):
        return '<User %r>' % self.name
    
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'address': self.address
        }
