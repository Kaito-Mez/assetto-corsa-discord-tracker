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

books = {"a_setup":False, "c_setup":False, "r_setup":False}
'''The discord books that are messaged to the server'''

'''Discord event handlers and other discord functions'''

@client.event
async def on_ready():
    print("Bot Online!")
    print("Name: {}".format(client.user.name))
    print("ID: {}".format(client.user.id))
    print("Version: {}".format(discord.__version__))
    print(discord.opus.is_loaded())

    if books["c_setup"] == False:
        activity, race, car, results = _get_channel_objects()
        await activity.purge()
        await race.purge()
        await car.purge()
        await results.purge()

    url = "ws://127.0.0.1:30001"
    await socket.connect(url)

    
@client.event   
async def on_raw_reaction_add(payload:discord.RawReactionActionEvent):
    member = payload.member
    emoji = payload.emoji
    message_id = payload.message_id    
    
    if client.user == member:
        return

    for book in books["racer_info"]:
        if book.message.id == message_id:
            await book.handle_react(emoji, member, message_id)
    
async def send_results_book():
    '''Sends the results information'''
    async def apply_mod(results_book):
        '''applies the mods to the page'''            
        fields = []

        results = get_race_results()

        winning_car = results[0].car

        for result in results:
            field = {"name":_format_player_name(result.guid), "inline":True, "value":_format_ms(result.laptime)}
            fields.append(field)
        date = "Last Updated: " + datetime.now().strftime("%H:%M:%S %d/%m/%Y")
        results_book.files = [(discord.File(f"database/car_images/{winning_car}.jpg", filename=f"{winning_car}.jpg"))]
        results_book.modify_page(1, False, fields = fields,  footer = {"text": date}, description = _format_player_name(results[0].guid), image = {"url":f"attachment://{winning_car}.jpg"})
        await results_book.update_page()

    _, _, _, results = _get_channel_objects()


    activity_book = discordBook(client, False, "models/templates/race_results.json")
    await activity_book.send_book(channel=results)

    await apply_mod(activity_book)
        

async def update_activity_book():
    '''Sets up and sends all relevant activity books to the server'''

    async def apply_mod(activity_book):
        '''applies the mods to the page'''            
        fields = [
                {
                    "name": _format_car_name(most_recent.car),
                    "inline": True,
                    "value": _format_ms(most_recent.laptime)
                },
                {
                    "name": "Average Time:",
                    "inline": True,
                    "value": _format_ms(get_average_laptime())
                }
            ]

        date = "Last Updated: " + datetime.now().strftime("%H:%M:%S %d/%m/%Y")
        activity_book.files = [(discord.File(f"database/car_images/{most_recent.car}.jpg", filename=f"{most_recent.car}.jpg"))]
        activity_book.modify_page(1, False, fields = fields, title=_format_player_name(most_recent.guid), footer = {"text": date}, image = {"url":f"attachment://{most_recent.car}.jpg"})
        await activity_book.update_page()
    

    most_recent = get_most_recent_lap()

    activity, _, _, _ = _get_channel_objects()

    
    if "activity" in books.keys():
        activity_book = books["activity"]
        if most_recent:
            await apply_mod(activity_book)
        books["activity"] = activity_book

    
    elif not books["a_setup"]:
        books["a_setup"] = True
        activity_book = discordBook(client, False, "models/templates/most_recent_lap.json")
        await activity_book.send_book(channel=activity)
        books["activity"] = activity_book

        if most_recent:
            await apply_mod(activity_book)
        
        books["a_setup"] = False

async def update_racer_books():
    '''Sets up the racer books and sends/updates them'''
    
    async def apply_mod(racer_book: discordBook, guid):
        cars_by_laptime = get_players_cars_ranked_by_laptime(guid)
        cars_by_playtime = get_players_cars_ranked_by_playtime(guid)

        fav_car = cars_by_playtime[0]
        fastest_car = cars_by_laptime[0]

        description1 = _format_car_name(fastest_car)
        description2 = _format_car_name(fav_car)


        fields1 = []
        for car in cars_by_laptime:
            laptime = get_player_fastest_lap_in_car(guid, car)
            if laptime:
                laptime = _format_ms(laptime.laptime)
            else: 
                laptime = "N/A"
            field = {"name":_format_car_name(car) + ":", 'inline':True, "value":laptime}
            fields1.append(field)
        
        fields2 = []

        for car in cars_by_playtime:
            field = {"name":_format_car_name(car) + ":", 'inline':True, "value":_format_seconds(get_player_playtime_in_car(guid, car))}
            fields2.append(field)
        

        author = {"name":_format_player_name(guid)}

        date = "Last Updated: " + datetime.now().strftime("%H:%M:%S %d/%m/%Y")
        racer_book.files = []
        racer_book.files.append(discord.File(f"database/car_images/{fastest_car}.jpg", filename=f"{fastest_car}.jpg"))
        racer_book.files.append(discord.File(f"database/car_images/{fav_car}.jpg", filename=f"{fav_car}.jpg"))
        racer_book.modify_page(1, False, fields=fields1, description = description1, footer={"text":date}, image={"url":f"attachment://{fastest_car}.jpg"}, author=author)
        racer_book.modify_page(2, False, fields=fields2, description = description2, footer={"text":date}, image={"url":f"attachment://{fav_car}.jpg"}, author=author)

        await racer_book.update_page()
    


    _, racer_info_channel, _, _ = _get_channel_objects()

    if "racer_info" in books.keys():
        racer_info_books = books["racer_info"]

        print(len(books["racer_info"]), len(get_all_players()))
        if len(books["racer_info"]) != len(get_all_players()):
            num = len(get_all_players()) - len(books["racer_info"])
            for _ in range(num):
                racer_book = discordBook(client, True, "models/templates/racer_info.json")
                await racer_book.send_book(channel= racer_info_channel)
                racer_info_books.append(racer_book)


        for index, player in enumerate(get_players_by_most_playtime()):
            await apply_mod(racer_info_books[index], player)
        
        
        books["racer_info"] = racer_info_books
    
    elif not books["r_setup"]:
        books["r_setup"] = True
        racer_info_books = []
        books["racer_info"] = racer_info_books
        for player in get_all_players():
            racer_book = discordBook(client, True, "models/templates/racer_info.json")
            racer_info_books.append(racer_book)

            await racer_book.send_book(channel= racer_info_channel)
            await apply_mod(racer_book, player)
        books["r_setup"] = False
        if racer_info_books != []:
            books["racer_info"] = racer_info_books


    

async def update_car_books():
    '''Sets up the car books and sends/updates them'''

    async def apply_mod(car_book: discordBook, car):

        lap = get_car_fastest_lap(car)
        laptime = "N/A"
        player = "N/A"
        if lap:
            laptime = _format_ms(lap.laptime)
            player = _format_player_name(lap.guid)
            
        playtime = get_car_playtime(car)
        fields = [
            {
                "name": "Fastest Lap:",
                "inline": True,
                "value": laptime
            },
            {
                "name": "Lap Set By:",
                "inline": True,
                "value": player
            },
            {
                "name": "Total Race Time:",
                "inline": False,
                "value" : _format_seconds(playtime)
            }

        ]
        title = _format_car_name(car)
        date = "Last Updated: " + datetime.now().strftime("%H:%M:%S %d/%m/%Y")
        car_book.files = [(discord.File(f"database/car_images/{car}.jpg", filename=f"{car}.jpg"))]
        car_book.modify_page(1, False, fields=fields, title=title, footer={"text":date}, image={"url":f"attachment://{car}.jpg"})

        await car_book.update_page()


    cars = get_cars_ranked_by_laptime()

    _, _, car_info_channel, _ = _get_channel_objects()

    if "car_info" in books.keys():
        car_info_books = books["car_info"]

        for index, car in enumerate(cars):
            await apply_mod(car_info_books[index], car)
        
        books["car_info"] = car_info_books
    
    elif not books["c_setup"]:
        books["c_setup"] = True
        car_info_books = []
        for car in cars:
            car_book = discordBook(client, False, "models/templates/car_info.json")
            car_book.data_file = f"database/cars/{car}.json"
            car_info_books.append(car_book)

            await car_book.send_book(channel= car_info_channel)
            await apply_mod(car_book, car)
        books["c_setup"] = False
        books["car_info"] = car_info_books



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

def _format_seconds(s):

    return str(timedelta(seconds=int(s)))


def _format_car_name(name):
    return get_car_name(name)

def _format_player_name(guid):
    return get_player_name(guid)


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
async def on_lap(session_type):
    '''On lap completed'''

    await update_activity_book()
    if session_type != "Practice":
        await update_racer_books()
        await update_car_books()

@socket.on("connection_closed")
async def on_connection_closed(session_type):
    '''On player leaves'''
    if session_type != "Practice":
        await update_racer_books()
        await update_car_books()

@socket.on("new_session")
async def on_new_session(session_type):
    '''When a new session starts'''
    print("New session", session_type)
    if session_type == "Practice":
        await update_activity_book()
        await set_practice_perms()
    else:
        await update_activity_book()
        await update_racer_books()
        await update_car_books()
        await set_qual_perms()

@socket.on("end_session")
async def on_end_session():
    '''On server shutdown'''
    print("On_end_session not implemented")
    await send_results_book()
    await set_race_perms()

if __name__ == "__main__":

    channels = get_channels()
    client.run(get_token())