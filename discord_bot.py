from models.disc_gui import discordBook
from dataframe_query import *
import discord
import socketio
from json import load

intents = discord.Intents.all()
'''Discord intents'''
client = discord.Client(intents=intents)
'''Discord client'''
socket = socketio.Client()
'''Socket client'''

channels = {}
'''The text channels that the bot sends to'''

car_info = None

racer_info = None

'''Discord event handlers and other discord functions'''

@client.event
async def on_ready():
    print("Bot Online!")
    print("Name: {}".format(client.user.name))
    print("ID: {}".format(client.user.id))
    print("Version: {}".format(discord.__version__))
    print(discord.opus.is_loaded())

def on_practice_start():
    '''Sets up the server when practice session starts'''
    print("Not Implemented")

def on_qualification_start():
    '''Sets up the server when qualification session staarts'''
    print("Not Implemented")

def on_race_start():
    '''Sets up the server when race session starts'''
    print("Not implemented")

'''Bot config functions'''

def get_token():
    with open("config/discordToken.txt", "r") as f:
        token = f.readline()
        return token

def get_channels():
    '''Loads the channels that the bot sends to''' 
    with open("config/channels.json", "r") as f:
        loaded_channels = load(f)

    return loaded_channels


'''Socket Event Handlers'''

@socket.on("connect")
def connect():
    print("Client Connected to assetto")

@socket.on("lap_completed")
def on_lap(data):
    print("Lap_completed not implemented")

@socket.on("connection_closed")
def on_connection_closed(data):
    print("Lap_completed not implemented")

@socket.on("end_session")
def on_end_session(data):
    print("On_end_session not implemented")

if __name__ == "__main__":
    url = "ws://127.0.0.1:30001"

    channels = get_channels()
    socket.connect(url)
    client.run(get_token())