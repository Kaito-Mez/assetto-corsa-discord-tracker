import socketio

sio = socketio.Client()

@sio.event
def connect():
    print("connected ")
    #print(sio.emit("authenticate", "admin"))
    print(sio.emit("enable_realtime_report", 500))
    print(sio.emit('broadcast_message', "test"))

@sio.on("chat")
def on_message(data):
    print(data)
    print("chat message")

@sio.on("lap_completed")
def on_collide(data):
    print(data)
    print("collide")
@sio.on("car_info")
def on_collided(data):
    print(data)
    print("collide")

@sio.on("car_update")
def d(data):
    print(data)
    print("collide")

sio.connect("http://192.168.1.200:30000")
print("here")

print(sio.emit("authenticate", "admin"))
print(sio.emit("enable_realtime_report", 500))
print(sio.emit('broadcast_message', "test"))
print(sio.emit("get_car_info", 10))