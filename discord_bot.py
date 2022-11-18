from models.disc_gui import discordBook
from dataframe_query import *
import discord
import socketio
from datetime import datetime, timedelta
import asyncio
from json import load

intents = discord.Intents.all()
'''Discord intents'''
client = discord.Client(intents=intents)
'''Discord client'''
socket = socketio.AsyncClient()
'''Asyncronous Socket client'''

channels = {}
'''The text channels that the bot sends to'''

books = {}
'''The discord books that are messaged to the server'''

car_info = None

racer_info = []

'''Discord event handlers and other discord functions'''

@client.event
async def on_ready():
    print("Bot Online!")
    print("Name: {}".format(client.user.name))
    print("ID: {}".format(client.user.id))
    print("Version: {}".format(discord.__version__))
    print(discord.opus.is_loaded())

    url = "ws://127.0.0.1:30001"
    await socket.connect(url)
    
    await update_activity_book()
    await asyncio.sleep(5)
    await update_activity_book()


async def update_activity_book():
    '''Sets up and sends all relevant activity books to the server'''

    async def apply_mod(activity_book):
        '''applies the mods to the page'''            
        fields = [
                {
                    "name": _convert_car_name(most_recent.car),
                    "inline": False,
                    "value": _format_ms(most_recent.laptime)
                },
                {
                    "name": "Average Time:",
                    "inline": False,
                    "value": _format_ms(get_average_laptime())
                }
            ]

        date = "Lap Completed At: " + datetime.now().strftime("%H:%M:%S %d/%m/%Y")
        activity_book.modify_page(1, False, fields = fields, title=most_recent.player, footer = {"text": date})
        await activity_book.update_page()
    

    most_recent = get_most_recent_lap()

    activity, _, _, _ = _get_channel_objects()

    #first time setup
    if "activity" in books.keys():
        activity_book = books["activity"]
        if most_recent:
            await apply_mod(activity_book)

    #update
    else:
        activity_book = discordBook(client, False, "models/templates/most_recent_lap.json")   
        books["activity"] = activity_book
        await activity_book.send_book(channel=activity)

        if most_recent:
            await apply_mod(activity_book)

async def update_car_books():
    '''Sets up the car books and sends/updates them'''



async def set_practice_perms():
    '''Sets up the server when practice session starts'''

    activity, racer_info, car_info, results = _get_channel_objects()

    guild = _get_guild_object()

    hide = _get_hide_overwrite()
    show = _get_show_overwrite()

    await activity.set_permissions(guild.default_role, overwrite=show)
    await racer_info.set_permissions(guild.default_role, overwrite=hide)
    await car_info.set_permissions(guild.default_role, overwrite=hide)
    await results.set_permissions(guild.default_role, overwrite=hide)

async def set_qual_perms():
    '''Sets up the server when qualification session staarts'''
    activity, racer_info, car_info, results = _get_channel_objects()

    guild = _get_guild_object()
    
    hide = _get_hide_overwrite()
    show = _get_show_overwrite()

    await activity.set_permissions(guild.default_role, overwrite=show)
    await racer_info.set_permissions(guild.default_role, overwrite=show)
    await car_info.set_permissions(guild.default_role, overwrite=show)
    await results.set_permissions(guild.default_role, overwrite=hide)

async def set_race_perms():
    '''Sets up the server when race session starts'''
    activity, racer_info, car_info, results = _get_channel_objects()

    guild = _get_guild_object()

    show = _get_show_overwrite()

    await activity.set_permissions(guild.default_role, overwrite=show)
    await racer_info.set_permissions(guild.default_role, overwrite=show)
    await car_info.set_permissions(guild.default_role, overwrite=show)
    await results.set_permissions(guild.default_role, overwrite=show)

def _format_ms(ms):
    minutes = (ms // 60000)
    ms -= 60000 * minutes
    

    seconds = ms // 1000
    ms -= 1000 * seconds

    minutes = str(int(minutes))
    seconds = str(int(seconds))
    ms = str(int(ms))

    formatted = f"{minutes.zfill(2)}:{seconds.zfill(2)}.{ms.zfill(3)}"
    return formatted


def _convert_car_name(name):
    return "implement convert car name " + name

def _get_hide_overwrite():
    '''returns an overwrite object that has no permissions'''
    overwrite = discord.PermissionOverwrite.from_pair(discord.Permissions.none(), discord.Permissions.all())
    return overwrite

def _get_show_overwrite():
    '''Returns an overwrite object that has read messages and history'''
    overwrite = _get_hide_overwrite()
    overwrite.update(
        read_messages = True, 
        read_message_history = True
        )

    return overwrite

def _get_guild_object() -> discord.Guild:
    return client.get_guild(channels["guild"])

def _get_channel_objects() -> tuple[discord.TextChannel,discord.TextChannel,discord.TextChannel,discord.TextChannel]:
    '''Returns the discord channel objects `activity`, `racer-info`, `car-info`, `results`'''
    activity = client.get_channel(channels["activity"])
    racer_info = client.get_channel(channels["racer-info"])
    car_info = client.get_channel(channels["car-info"])
    results = client.get_channel(channels["results"])

    return activity, racer_info, car_info, results

'''Bot config functions'''

def get_token():
    with open("config/discordToken.txt", "r") as f:
        token = f.readline()
        return token

def get_channels():
    '''Loads the channels that the bot sends to''' 
    with open("config/channels.json", "r") as f:
        loaded_channels = dict(load(f))

    return loaded_channels


'''Socket Event Handlers'''

@socket.on("connect")
async def on_connect():
    '''On connection with the assetto manager'''
    print("Client Connected to assetto")


@socket.on("lap_completed")
async def on_lap(data):
    '''On lap completed'''
    print("Lap_completed not implemented")

@socket.on("connection_closed")
async def on_connection_closed(data):
    '''On player leaves'''
    print("Lap_completed not implemented")

@socket.on("end_session")
async def on_end_session(data):
    '''On server shutdown'''
    print("On_end_session not implemented")

if __name__ == "__main__":

    channels = get_channels()
    client.run(get_token())