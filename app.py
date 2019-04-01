from flask import Flask, render_template, request,send_from_directory
from flask_socketio import SocketIO
from flask_login import LoginManager,login_required

import os
import json

CWD=os.getcwd()
os.environ['CWD']=CWD


import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.NOTSET)
login_manager=LoginManager()
login_manager.login_view = "login"

app = Flask(__name__,template_folder='template')
app.secret_key="Kawi12!Ea$4sD*"
print(__name__)
login_manager.init_app(app)
app.config['CWD']=CWD
import login_management

import app_helper