# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 21:01:08 2022

@author: Admin
"""

import sys
from flask import render_template, redirect, url_for, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def index():
    return jsonify([e.serialize() for e in User.query.all()])
def store():
    db.session.add(User(name="mujir", age="24", address="pasuruan"))
    db.session.commit()
    return "user"
def show(userId):
    return "user"
def update(userId):
    return "user"
def delete(userId):
    return "user"

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.String(120))
    address = db.Column(db.String(120))
    
    def __init__(self, name, age, address):
        self.name = name
        self.age = age
        self.address = address
        
    def __repr__(self):
        return '<User %r>' % self.name
    
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'address': self.address
        }