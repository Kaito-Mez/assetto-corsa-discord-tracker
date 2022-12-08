from datetime import datetime
import json
from time import sleep
import socketio
from flask import Flask
from flask_socketio import SocketIO
from json import loads
from dao import Dao
from models.lap_data import LapData
from models.race_data import RaceData
from models.session_data import SessionData
from rcon.source import Client as rconClient

assetto = socketio.Client()
'''SocketIO client that connects to the assetto corsa server'''

discord_app = Flask(__name__)
'''The app wrapper for the discord socket server'''

discord = SocketIO(discord_app)
'''The discord Socket server'''

current_clients = {}
'''Players currently connected to the server format {car_id:session_data}'''

current_session = []
'''Practice, Qualification or Race'''

'''
Assetto Socket Event Handlers
'''
@assetto.event
def connect():
    '''Setup on connection to plugin'''

    print("connected ")
    assetto.emit("authenticate", get_password())

    on_session_info(get_session_from_file())

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

    car_id = lap_data["car_id"]
    lap = LapData(
        json_lap=lap_data, 
        session_data=current_clients[car_id], 
        session_type=current_session
        )

    print(lap.to_json())
    newline()

    dao = Dao("laps.json")
    dao.save(lap.to_json())

    discord.emit("lap_completed", current_session[0])


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
def on_end_session(filepath):
    '''Only triggers when the server closes
    fails if no write perms'''
    print("End session")
    print(filepath)
    print(current_clients)
    if current_session[0] == "Race":
        keys = []
        for car_id in current_clients.keys():
            keys.append(car_id)
        
        for car_id in keys:
            on_player_leave({"car_id":car_id}, remove=False)
        
        discord.emit("end_session")
        print("emmitted")

@assetto.on("client_loaded")
def on_player_join(join_data):
    '''Sets up a new session class when a player joins'''

    print("Player Joined")
    print(join_data)
    newline()
    start_time = datetime.now()
    new_session = SessionData(start_time, join_data)
    current_clients.update({new_session.car_id:new_session})

    try:
        assetto.emit("get_car_info", new_session.car_id)
    except Exception as e:
        print(e)

@assetto.on("connection_closed")
def on_player_leave(leave_data, remove = True):
    '''Finalizes session data when a player leaves'''

    print("Player Left")
    print(leave_data)
    newline()
    end_time = datetime.now()
    if remove:
        session = current_clients.pop(leave_data["car_id"])
    else:
        session = current_clients[leave_data["car_id"]]
    session.session_end(end_time)

    print("DO SOMETHING WITH SESSION DATA")
    print(session)
    print(current_clients)

    dao = Dao("sessions.json")
    dao.save(session.to_json())
    newline()

    discord.emit("connection_closed", current_session[0])


@assetto.on('new_session')
def on_session_start(session_data):
    '''Sets current_session when a new session starts'''
    print("Start session")
    print(session_data)
    current_session.clear()
    sessions = ["Practice", "Qualification", "Race"]
    
    current_session.append(sessions[session_data["current_session_index"]])
    print(current_session)
    newline()

    if (current_session[0] != "Practice"):
        with rconClient('192.168.1.200', 8006, passwd=get_password()) as rcon_client:
            responses = []
            responses.append(rcon_client.run('set', 'Extra.AiParams.PlayerRadiusMeters', '0'))
            responses.append(rcon_client.run('set', 'Extra.AiParams.MinSpawnProtectionTimeSeconds', '0'))
            responses.append(rcon_client.run('set', 'Extra.AiParams.MaxSpawnProtectionTimeSeconds', '0'))
            responses.append(rcon_client.run('set', 'Extra.AiParams.MaxAiTargetCount', '0'))
            responses.append(rcon_client.run('set', 'Extra.AiParams.AiPerPlayerTargetCount', '0'))
            print(responses)

    discord.emit("new_session", current_session[0])

@assetto.on("session_info")
def on_session_info(session_data):
    '''Sets current_session on connection to the plugin'''
    print("Session info")
    print(session_data)
    print(current_session)
    newline()

    on_session_start(session_data)


'''Discord Socket Event Handlers'''

@discord.on("connect")
def on_disc_connect():
    '''On connection to the assetto server'''
    print("Connected To discord")
    assetto.emit("get_session_info")


def get_session_from_file():
    '''Gets the session index from the json for first boot'''

    with open("database/current_session.json", "r") as f:
        data = json.load(f)
    
    return data

def connect_sockets(url):
    '''Connect to the plugin via socketio at url'''
    assetto.connect(url)
    discord.run(discord_app, host='0.0.0.0', port=30001)

def newline():
    print("####################################################################################")

def get_password():
    '''Gets the server password'''
    with open("./config/serverPassword.txt", "r") as f:
        return f.readline()

if __name__ == "__main__":
    url = "http://192.168.1.200:30000"
    connect_sockets(url)
