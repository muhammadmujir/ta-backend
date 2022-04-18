# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 12:21:35 2022

@author: Admin
"""

from singleton import Singleton
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from config import SQLALCHEMY_DATABASE_URI

class Application(metaclass=Singleton):
    def __init__(self):
        self.app = Flask(__name__)
        store = {'default': SQLAlchemyJobStore(url=SQLALCHEMY_DATABASE_URI)}
        self.scheduler = BackgroundScheduler(jobstores=store)