# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 20:35:23 2021

@author: Admin
"""

#Import necessary libraries
from flask import Flask, render_template, Response, request, jsonify, session, copy_current_request_context
from multiprocessing import Process
import cv2
import torch
from torchvision import datasets, transforms
from crowd_counting.inceptionresnetv2 import InceptionResNetV2
from routes.user_bp import user_bp
from routes.camera_bp import camera_bp
from routes.static_bp import static_bp
from routes.statistic_bp import statistic_bp
from database import Database
from flask_migrate import Migrate
from models.user import User
from models.camera import Camera
from models.camera_owner import CameraOwner
from models.statistic import Statistic
from responses.exceptions.exception import exception_bp
import numpy as np
import PIL.Image as Image
from matplotlib import cm
import time
from flask_socketio import SocketIO, emit, disconnect, join_room, leave_room
from threading import Lock
from application import Application

#Initialize the Flask app
# app = Flask(__name__)
app = Application().app
app.config.from_object('config')
app.register_blueprint(user_bp)
app.register_blueprint(camera_bp)
app.register_blueprint(exception_bp)
app.register_blueprint(static_bp)
app.register_blueprint(statistic_bp)
db = Database().db
db.init_app(app)
migrate = Migrate(app, db)
async_mode = None
socketio = SocketIO(app, async_mode=async_mode)
thread = dict()
thread_lock = Lock()
Application().scheduler.start()

# camera = cv2.VideoCapture(0)
# if not camera.isOpened():
#     print("Cannot open camera")
    
#init model
# model = InceptionResNetV2().cpu()
# checkpoint = torch.load("D:\\TA\\Dataset\\Result\\0model_best.pth.tar")
# model.load_state_dict(checkpoint['state_dict'])
# transform=transforms.Compose([
#                       transforms.ToTensor(),transforms.Normalize(
#                           mean=[0.485, 0.456, 0.406],
#                           std=[0.229, 0.224, 0.225]),
#                   ])


# def gen_frame():
#     delay = 10 # 1 minute
#     start = time.time()
#     while True:
#         success, frame = camera.read()
#         if not success:
#             break
#         else:
#             if (time.time() - start >= delay):
#                 im = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#                 im = Image.fromarray(np.uint8(np.array(im)))
#                 im = transform(im).cpu()
#                 # im.save("C:\\Users\\Admin\\Desktop\\TA\\Dataset\\UCF-QNRF_ECCV18\\Test\\debug\\coba.jpg")
#                 # calculate crowd count
#                 output = model(im.unsqueeze(0))
#                 print("Predicted Count : ",int(output.detach().cpu().sum().numpy()))
#                 start = time.time()
#             ret, buffer = cv2.imencode('.jpg', frame)
#             frame = buffer.tobytes()
#             yield(b'--frame\r\n'
#                   b'Content-Type: image/jpeg\r\n\r\n'+frame+b'\r\n')

# @app.route('/')
# def index():
#     return render_template('websocket.html', async_mode=async_mode)

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/video_feed')
# def video_feed():
#     # camera = cv2.VideoCapture(0)
#     return Response(gen_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/video_stop')
# def video_stop():
#     camera.release()
#     return 'cemara stop'

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    
@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

@app.errorhandler(404)
def handle_404_error(err):
    response = {"code": 404, "status": "Not Found", "data": None, "errors": ["Not Found"]}
    return jsonify(response), 404

def calculate_crowd_counting(message):
    start = time.time()
    while True:
        socketio.sleep(3)
        # with app.app_context():
        #     socketio.emit('my_response', {'data': message['data'], 'count': session.get('receive_count', 0) }, namespace='/test')
        with app.test_request_context('/'):
            session['receive_count'] = session.get('receive_count', 0) + 1
            socketio.emit('my_response', {'data': message['data'], 'count': session.get('receive_count', 0) }, namespace='/test', room=message['data'])
        # if (time.time() - start == 30):
        #     session['receive_count'] = session.get('receive_count', 0) + 1
        #     emit('my_response',
        #           {'data': 'Streaming', 'count': session['receive_count']})
        #     start = time.time()
        
        # if (session.get('receive_count', 0) > 10):
        #     break
        
@socketio.on('my_event', namespace='/test')
def test_message(message):
    global thread
    join_room(message['data'])
    # with thread_lock:
    #     # print("masuk event")
    #     if thread is None:
    #         thread = socketio.start_background_task(calculate_crowd_counting(message))
    # thread_lock.acquire()
    if not message['data'] in thread.keys():
        thread[message['data']] = socketio.start_background_task(calculate_crowd_counting(message))
    # thread_lock.release()
    # session['receive_count'] = session.get('receive_count', 0) + 1
    # emit('my_response',
    #       {'data': message['data'], 'count': session['receive_count']})

@socketio.on('join', namespace='/test')
def join():
    print("berhasil join")
    join_room("mujir", namespace='/test')

@socketio.on('leave', namespace='/test')
def leave():
    print("berhasil leave")
    leave_room("mujir", namespace='/test')
    
@socketio.on('my_broadcast_event', namespace='/test')
def test_broadcast_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']},
         broadcast=True)


@socketio.on('connect', namespace='/test')
def connect():
    # global thread
    # with thread_lock:
    #     if thread is None:
    #         thread = socketio.start_background_task(calculate_crowd_counting)
    emit('my_response',
          {'data': 'Connected', 'count': session.get('receive_count', 0)})
    
@socketio.on('disconnect_request', namespace='/test')
def disconnect_request():
    @copy_current_request_context
    def can_disconnect():
        disconnect()

    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'Disconnected!', 'count': session['receive_count']},
         callback=can_disconnect)

# from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
# from config import SQLALCHEMY_DATABASE_URI
# # scheduler = BackgroundScheduler()
# store = {'default': SQLAlchemyJobStore(url=SQLALCHEMY_DATABASE_URI)}
# scheduler = BackgroundScheduler(jobstores=store)

# def trainModel():
#     print("coba")
#     scheduler.print_jobs()

# def schedule(jobId, isAddJob = True):
#     # scheduler.add_job(trainModel, 'interval', minutes=1, id='camera1')
#     if isAddJob:
#         scheduler.add_job(trainModel, 'cron', hour='6-23', minute=25, id=jobId)
#         scheduler.start()
#         scheduler.print_jobs()
#     else:    
#         if scheduler.get_job(jobId):
#             scheduler.remove_job(jobId)
#             scheduler.print_jobs()
    

# @app.route('/schedule', methods=['GET'])
# def scheduleJob():
#     operation = True if request.args.get('isAddJob') == 'true' else False
#     schedule(request.args.get('job'), operation)
#     return 'Schedule Success'

if __name__ == "__main__":
    # app.run(debug=True)
    socketio.run(app, ssl_context=None, debug=True)