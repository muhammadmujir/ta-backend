# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 23:27:17 2022

@author: Admin
"""
from flask import Blueprint, request
from application import Application
from threading import Lock
from flask import copy_current_request_context
from flask_socketio import emit, disconnect, join_room, leave_room
import time
import cv2
import PIL.Image as Image
import numpy as np
from crowd_counting.crowd_counting import *
from flask_socketio import rooms
import json
import time

# socketio_bp = Blueprint('socket_bp', __name__)
app = Application().app
socketio = Application().socketio
thread = dict()
workers = dict()
thread_lock = Lock()

class Worker(object):
    
    isContinue = False
    
    def __init__(self, data):
        self.isContinue = True
        self.data = data
        self.clientCount = 0
        
    def doWork(self):
        with app.test_request_context('/'):
            camera = cv2.VideoCapture(self.data['rtspAddress'])
            # camera = cv2.VideoCapture("C:\\Users\\Admin\\Downloads\\videoplayback (1).mp4")
            # camera = cv2.VideoCapture("http://192.168.43.194:5001/video/1")
            # i = 0
            start = time.time()
            while self.isContinue:
                # socketio.sleep(5)
                success, frame = camera.read()
                if not success:
                    break
                elif time.time() - start >= 20:
                    start = time.time()
                    im = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    im = Image.fromarray(np.uint8(np.array(im)))
                    # im.save("C:\\Users\\Admin\\Downloads\\Crowd\\{}.jpg".format(i))
                    im = transform(im).cpu()
                    # calculate crowd count
                    output = model(im.unsqueeze(0))
                    crowd = output.detach().cpu().sum().numpy()
                    print("Crowd: ", crowd)
                    print("------------counting------------------------")
                    socketio.emit('my_response', {'count': int(crowd)}, room=str(self.data['id']), namespace='/camera')
                    # i += 1
            
    def stop(self):
        with app.app_context():
            self.isContinue = False
    
    def updateClientCount(self, num):
        self.clientCount += num
        
@socketio.on('join', namespace='/camera')
def join(data):
    data = json.loads(data)
    # ketika sudah terkonek ke websocket, secara default user masuk ke room yang isinya 
    # hanya user itu sendiri. Hal, berguna untuk mengirim direct message
    userNotInRoom = len(socketio.server.rooms(request.sid, namespace="/camera")) == 1
    if userNotInRoom:
        join_room(str(data['id']), namespace='/camera')
        if not data['id'] in workers.keys():
            workers[data['id']] = Worker(data)
        workers[data['id']].updateClientCount(1)
        if not data['id'] in thread.keys():
            thread[data['id']] = socketio.start_background_task(workers[data['id']].doWork)
    else:
        print("sudah masuk room")

@socketio.on('leave', namespace='/camera')
def leave(data):
    data = json.loads(data)
    leave_room(str(data['id']), namespace='/camera')
    workers[data['id']].updateClientCount(-1)
    print("Count: "+str(workers[data['id']].clientCount))
    if workers[data['id']].clientCount <= 0:
        workers[data['id']].stop()
        del thread[data['id']]
        del workers[data['id']]
        

@socketio.on('connect', namespace='/camera')
def connect():
    # global thread
    # with thread_lock:
    #     if thread is None:
    #         thread = socketio.start_background_task(calculate_crowd_counting)
    emit('connect_response', {'data': 'Connected'}, room=request.sid)
    
@socketio.on('disconnect_request', namespace='/camera')
def disconnect_request():
    @copy_current_request_context
    def can_disconnect():
        disconnect()

    emit('my_response',
         {'data': 'Disconnected!', 'count': 0},
         callback=can_disconnect)

# def crowdCounting(data):
#     with app.app_context():
#         # camera = cv2.VideoCapture(data['rtspAddress'])
#         camera = cv2.VideoCapture("C:\\Users\\Admin\\Downloads\\videoplayback (1).mp4")
#         while True:
#             socketio.sleep(5)
#             success, frame = camera.read()
#             if not success:
#                 break
#             else:
#                 im = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#                 im = Image.fromarray(np.uint8(np.array(im)))
#                 im = transform(im).cpu()
#                 # im.save("C:\\Users\\Admin\\Desktop\\TA\\Dataset\\UCF-QNRF_ECCV18\\Test\\debug\\coba.jpg")
#                 # calculate crowd count
#                 output = model(im.unsqueeze(0))
#                 crowd = output.detach().cpu().sum().numpy()
#                 print("counting")
#                 emit('my_response', {'count': int(crowd)}, room=data['id'])
                
# def calculate_crowd_counting(message):
#     start = time.time()
#     while True:
#         socketio.sleep(3)
#         # with app.app_context():
#         #     socketio.emit('my_response', {'data': message['data'], 'count': session.get('receive_count', 0) }, namespace='/camera')
#         with app.test_request_context('/'):
#             socketio.emit('my_response', {'data': message['data'], 'count': 0 }, namespace='/camera', room=message['data'])
#         # if (time.time() - start == 30):
#         #     session['receive_count'] = session.get('receive_count', 0) + 1
#         #     emit('my_response',
#         #           {'data': 'Streaming', 'count': session['receive_count']})
#         #     start = time.time()
        
#         # if (session.get('receive_count', 0) > 10):
#         #     break
        
# @socketio.on('my_event', namespace='/camera')
# def test_message(message):
#     global thread
#     join_room(message['data'])
#     # with thread_lock:
#     #     # print("masuk event")
#     #     if thread is None:
#     #         thread = socketio.start_background_task(calculate_crowd_counting(message))
#     # thread_lock.acquire()
#     if not message['data'] in thread.keys():
#         thread[message['data']] = socketio.start_background_task(calculate_crowd_counting(message))
#     # thread_lock.release()
#     # session['receive_count'] = session.get('receive_count', 0) + 1
#     # emit('my_response',
#     #       {'data': message['data'], 'count': session['receive_count']})
   
# @socketio.on('my_broadcast_event', namespace='/camera')
# def test_broadcast_message(message):
#     emit('my_response',
#          {'data': message['data'], 'count': 0},
#          broadcast=True)