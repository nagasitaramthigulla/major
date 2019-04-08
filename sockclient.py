try:
    from __main__ import socketio,threadPool,request
except:
    from app_helper import socketio,threadPool,request

client_dict = {}

@socketio.on('connected')
def greet(json):
    print(json)
    client_dict[json['hash']]=request.sid
    socketio.emit('json',{'message':'client session id:'+request.sid},room=request.sid)

@socketio.on('json')
def handle_json(json):
    socketio.emit('json',{'message':'received '+json['message']},room=request.sid)

    threadPool.condition.acquire()
    threadPool.put((json['message'],request.sid,socketio))
    threadPool.condition.notify()
    threadPool.condition.release()