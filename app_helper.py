from app import *
from actionThread import ThreadPool,CleanerThread
from flask_login import current_user


threadPool=ThreadPool(3)
cl=CleanerThread()
cl.start()

@app.route("/")
def app_base():
    return redirect('home')

@app.route('/home')
@login_required
def webprint():
    return render_template('socket_client.html',login=False) 

@app.route('/images/<path:path>')
def send_js(path):
    return send_from_directory(CWD+'\images', path)

@app.route('/res/<id>')
def display(id):
    with open(CWD+'\\template\\mapapi.txt') as f:
        api_key=f.read()
    return render_template('result.html', id = id,api_key=api_key,login=False)

@app.route('/results/<path:path>')
@login_required
def send_json(path):
    return send_from_directory(CWD+'\\results',path)

@app.route('/about')
def about():
    return render_template('about.html',login=not current_user.is_authenticated)

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

socketio = SocketIO(app)

import sockclient

socketio.run(app)