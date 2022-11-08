import socketio
from discord_bot import AssettoStatsBot
from models.lap_data import LapData
from models.session_data import SessionData
from models.player_data import PlayerData
from datetime import datetime

assetto = socketio.Client()
'''SocketIO client that connects to the assetto corsa server'''

#discord = AssettoStatsBot()
'''The discord client'''

current_clients = {}
'''Players currently connected to the server format {car_id:session_data}'''

current_session = []
'''Practice, Qualification or Race'''

'''
Event Handlers
'''
@assetto.event
def connect():
    '''Setup on connection to plugin'''

    print("connected ")
    assetto.emit("authenticate", "admin")
    assetto.emit("get_session_info")
    assetto.emit("broadcast_message", "UDP Manager Connected")

@assetto.on("chat")
def on_message(data):
    '''Prints chat messages'''
    print("chat message")
    print(data)
    newline()

@assetto.on("lap_completed")
def on_lap_completed(lap_data):
    '''Saves data every time a lap is completed'''
    print("Lap Completed:")
    newline()

    car_id = lap_data["car_id"]
    lap = LapData(lap_data, current_clients[car_id])

    print("DO SOMETHING WITH LAP DATA")
    print(lap.to_json())
    print(current_clients)
    newline()


# Triggered when "get_car_info" is emitted
@assetto.on("car_info")
def on_car_info(car_data):
    '''
    Called when get_car_info is emmited.\n
    Updates the relevant current session with session data.
    '''
    print("car_info")
    print((car_data))

    car_id = car_data["car_id"]

    current_clients[car_id].update_car_info(car_data)

    print(current_clients)
    newline()

@assetto.on("lap_split")
def on_lap_split(data):
    '''Doesn't work'''
    print("Lap Split:")
    print(data)
    newline()

@assetto.on("end_session")
def on_session_ends(data):
    '''Doesnt work'''
    print("End session")
    print(data)
    newline()

@assetto.on("client_loaded")
def on_player_join(join_data):
    '''Sets up a new session class when a player joins'''

    print("Player Joined")
    print(join_data)
    newline()
    start_time = datetime.now()
    new_session = SessionData(start_time, join_data)
    current_clients.update({new_session.car_id:new_session})

    assetto.emit("get_car_info", new_session.car_id)

@assetto.on("connection_closed")
def on_player_leave(leave_data):
    '''Finalizes session data when a player leaves'''

    print("Player Left")
    print(leave_data)
    newline()
    end_time = datetime.now()
    session = current_clients.pop(leave_data["car_id"])
    session.session_end(end_time)

    print("DO SOMETHING WITH SESSION DATA")
    print(session.to_json())
    print(current_clients)
    newline()


@assetto.on('new_session')
def on_session_start(session_data):
    '''Sets current_session when a new session starts'''
    print("Start session")
    print(session_data)
    current_session.clear()
    current_session.append(session_data["name"])
    print(current_session)
    newline()

@assetto.on("session_info")
def on_session_info(session_data):
    '''Sets current_session on connection to the plugin'''
    print("Session info")
    print(session_data)
    current_session.clear()
    current_session.append(session_data["name"])
    print(current_session)
    newline()


def connect(url):
    '''Connect to the plugin via socketio at url'''
    assetto.connect(url)

def newline():
    print("####################################################################################")



if __name__ == "__main__":
    url = "http://192.168.1.200:30000"

    connect(url)