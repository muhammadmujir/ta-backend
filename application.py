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
from flask_socketio import SocketIO, emit, disconnect, join_room, leave_room

class Application(metaclass=Singleton):
    def __init__(self):
        self.app = Flask(__name__)
        store = {'default': SQLAlchemyJobStore(url=SQLALCHEMY_DATABASE_URI)}
        self.scheduler = BackgroundScheduler(jobstores=store)
        # async_mode = None
        # self.socketio = SocketIO(self.app, async_mode=async_mode)
        # async_mode is not set, in order to enable automatic selection of an async mode
        # you'll get eventlet or gevent, depending on what you have installed.
        # https://stackoverflow.com/questions/51330473/gevent-gevent-websocket-not-being-used-by-flask-socketio
        self.socketio = SocketIO(self.app)