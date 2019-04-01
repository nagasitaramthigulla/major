from app import *
from actionThread import ThreadPool,CleanerThread


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
    with open(CWD+'\\results\\'+id+'.json') as f:
        jsondata=f.read()
    return render_template('result.html', id = id,jsondata=jsondata,login=False)

@app.route('/results/<path:path>')
@login_required
def send_json(path):
    return send_from_directory(CWD+'\\results',path)

socketio = SocketIO(app)

import sockclient

socketio.run(app)