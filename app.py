# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 20:35:23 2021

@author: Admin
"""

#Import necessary libraries
from flask import Flask, render_template, Response, request, jsonify
from multiprocessing import Process
import cv2
import torch
from torchvision import datasets, transforms
from crowd_counting.inceptionresnetv2 import InceptionResNetV2
from routes.user_bp import user_bp
from database import Database
from flask_migrate import Migrate
from models.user import User
from models.camera import Camera
from models.camera_owner import CameraOwner
from models.statistic import Statistic
from responses.exceptions.exception import exception_bp

#Initialize the Flask app
app = Flask(__name__)
app.config.from_object('config')
app.register_blueprint(user_bp)
app.register_blueprint(exception_bp)
db = Database().db
db.init_app(app)
migrate = Migrate(app, db)

# camera = cv2.VideoCapture(0)
# if not camera.isOpened():
#     print("Cannot open camera")
#     exit()
    
#init model
# model = InceptionResNetV2().cpu()
# checkpoint = torch.load("G:\\Dataset\\Result\\0model_best.pth.tar")
# model.load_state_dict(checkpoint['state_dict'])
# transform=transforms.Compose([
#                       transforms.ToTensor(),transforms.Normalize(
#                           mean=[0.485, 0.456, 0.406],
#                           std=[0.229, 0.224, 0.225]),
#                   ])

def gen_frame():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            # calculate crowd count
            # output = model(frame.unsqueeze(0))
            # prediction = output.detach().cpu()
            
            # concat frame one by one and show result
            yield(b'--frame\r\n'
                  b'Content-Type: image/jpeg\r\n\r\n'+frame+b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    camera = cv2.VideoCapture(0)
    return Response(gen_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_stop')
def video_stop():
    camera.release()
    return 'cemara stop'

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

if __name__ == "__main__":
    app.run(debug=True)