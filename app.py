from flask import Flask, render_template, request,send_from_directory
from flask_socketio import SocketIO

import os
import json

CWD=os.getcwd()
os.environ['CWD']=CWD

from actionThread import ThreadPool,CleanerThread

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


threadPool=ThreadPool(3)
cl=CleanerThread()
cl.start()

app = Flask(__name__,template_folder='template')
print(__name__)

@app.route('/')
def webprint():
    return render_template('socket_client.html') 

@app.route('/images/<path:path>')
def send_js(path):
    return send_from_directory(CWD+'\images', path)

@app.route('/res/<id>')
def display(id):
    with open(CWD+'\\results\\'+id+'.json') as f:
        jsondata=f.read()
    return render_template('result.html', id = id,jsondata=jsondata)

@app.route('/results/<path:path>')
def send_json(path):
    return send_from_directory(CWD+'\\results',path)

socketio = SocketIO(app)

import sockclient

if __name__=='__main__':
    socketio.run(app)