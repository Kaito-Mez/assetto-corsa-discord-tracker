from models.lap_data import LapData
from dao import Dao

def get_player_fastest_lap(guid) -> LapData or None:
    '''Gets the fasest lap of specified player'''

    fastest_lap = None

    dao = Dao("laps.json")
    all_laps = dao.get_dataframe()
    if all_laps.shape[0] > 0:
        #all_laps = all_laps[all_laps.session != "Practice"]
        player_laps = all_laps[all_laps.guid == guid]
        fastest_laps = player_laps[player_laps.laptime == player_laps.laptime.min()]

        try:
            fastest_lap_df = fastest_laps.iloc[0].to_dict()
            fastest_lap = LapData(json_lap_data = fastest_lap_df)
        except IndexError as e:
            pass

    return fastest_lap
    
def get_car_fastest_lap(car) -> LapData or None:
    '''Gets the fastest lap of specified car'''

    fastest_lap = None

    dao = Dao("laps.json")
    all_laps = dao.get_dataframe()

    if all_laps.shape[0] > 0:

        #all_laps = all_laps[all_laps.session != "Practice"]
        car_laps = all_laps[all_laps.car == car]
        fastest_laps = car_laps[car_laps.laptime == car_laps.laptime.min()]

        try:
            fastest_lap_df = fastest_laps.iloc[0].to_dict()
            fastest_lap = LapData(json_lap_data = fastest_lap_df)
        except IndexError as e:
            pass

    return fastest_lap

def get_player_fastest_lap_in_car(guid, car) -> LapData or None:
    '''Gets a specific players fastest lap in a specific car'''
    
    fastest_lap = None
    
    dao = Dao("laps.json")
    all_laps = dao.get_dataframe()
    if all_laps.shape[0] > 0:
        #all_laps = all_laps[all_laps.session != "Practice"]
        player_laps = all_laps[all_laps.guid == guid]
        car_laps = player_laps[player_laps.car == car]
        fastest_laps = car_laps[car_laps.laptime == car_laps.laptime.min()]

        try:
            fastest_lap_df = fastest_laps.iloc[0].to_dict()
            fastest_lap = LapData(json_lap_data = fastest_lap_df)
        except IndexError as e:
            pass

    return fastest_lap

def get_most_recent_lap():
    '''Returns the most recent lap'''

    most_recent = None
    lap = None

    dao = Dao("laps.json")
    
    all_laps = dao.get_dataframe()

    if all_laps.shape[0] > 0:
        try:
            most_recent = all_laps.iloc[-1].to_dict()
        except IndexError as e:
            pass
        

        if most_recent:
            lap = LapData(json_lap_data = most_recent)
            
    return lap

def get_average_laptime():
    '''Gets the average laptime of all laps'''

    dao = Dao("laps.json")
    all_laps = dao.get_dataframe()

    mean = all_laps.laptime.mean()

    return mean

def get_all_players():
    '''Returns all guids'''

    dao = Dao("laps.json")

    all_laps = dao.get_dataframe()

    all_players = []

    if all_laps.shape[0] > 0:
        all_registered = all_laps.guid.unique()

        for registered in all_registered:
            all_players.append(registered)
    
    return all_players

def get_player_playtime(guid):
    '''Gets a player's total playtime on the server in seconds'''

    dao = Dao("sessions.json")
    all_sessions = dao.get_dataframe()
    total_playtime = 0
    if all_sessions.shape[0] > 0:

        player_sessions = all_sessions[all_sessions.guid == guid]

        total_playtime = player_sessions.session_time.sum()

    return total_playtime

def get_player_playtime_in_car(guid, car):
    '''Gets a player's total playtime on the server in a specific car'''

    dao = Dao("sessions.json")
    all_sessions = dao.get_dataframe()

    total_time = 0

    if all_sessions.shape[0] > 0:

        player_sessions = all_sessions[all_sessions.guid == guid]
        car_sessions = player_sessions[player_sessions.car == car]
        total_time = car_sessions.session_time.sum()

    return total_time

def get_car_playtime(car):
    '''Gets the total playtime of a car regardless of player'''
    dao = Dao("sessions.json")
    all_sessions = dao.get_dataframe()
    session_time = 0

    if all_sessions.shape[0] > 0:
        car_sessions = all_sessions[all_sessions.car == car]
        session_time = car_sessions.session_time.sum()

    return session_time

def get_all_cars():
    '''Returns all car names'''

    dao = Dao("car_translate.json")

    all_cars = dao.get_json()

    return list(all_cars.keys())

def get_car_name(car):
    '''Return the actual name of a car based on its ID'''

    dao = Dao("car_translate.json")
    all_cars = dao.get_json()

    return all_cars[car]

def get_cars_ranked_by_laptime():
    '''Return a list of cars from fastest laptime to slowest'''

    def rule(lap:LapData):
        return lap.laptime

    all_cars = get_all_cars()

    no_laps = []
    ranked_laps = []

    for car in all_cars:
        fastest_lap = get_car_fastest_lap(car)
        if fastest_lap:
            ranked_laps.append(fastest_lap)
        else:
            no_laps.append(car)
    ranked_laps.sort(key = rule)
    
    ranked_cars = []

    for lap in ranked_laps:
        ranked_cars.append(lap.car)

    for car in no_laps:
        ranked_cars.append(car)
    
    return ranked_cars

def get_player_name(guid):
    '''returns a players current name using their guid'''
    dao = Dao("laps.json")
    all_laps = dao.get_dataframe()
    player_laps = all_laps[all_laps.guid == guid]
    most_recent_name = player_laps.iloc[-1].player

    return most_recent_name

def get_players_cars_ranked_by_playtime(guid):
    '''Returns the name of the players cars from most played to least'''

    def sort(time_car_pair):
        return list(time_car_pair.keys())[0]


    dao = Dao("sessions.json")
    all_sessions = dao.get_dataframe()

    if all_sessions.shape[0] > 0:

        player_sessions = all_sessions[all_sessions.guid == guid]

        no_time = []
        ranked_time = []

        for car in get_all_cars():
            time = player_sessions[player_sessions.car == car].session_time.sum()
            if time == 0:
                no_time.append(car)
            else:
                ranked_time.append({time:car})

        ranked_time.sort(key=sort, reverse=True)

        sorted_cars = []

        for time in ranked_time:
            sorted_cars.append(list(time.values())[0])
        
        for car in no_time:
            sorted_cars.append(car)
    else:
        sorted_cars = get_all_cars()
    return sorted_cars
    
def get_players_cars_ranked_by_laptime(guid):
    '''Return a list of cars from fastest laptime to slowest for a player'''

    def rule(lap:LapData):
        return lap.laptime

    all_cars = get_all_cars()

    no_laps = []
    ranked_laps = []

    for car in all_cars:
        fastest_lap = get_player_fastest_lap_in_car(guid, car)
        if fastest_lap:
            ranked_laps.append(fastest_lap)
        else:
            no_laps.append(car)
    ranked_laps.sort(key = rule)
    
    ranked_cars = []

    for lap in ranked_laps:
        ranked_cars.append(lap.car)

    for car in no_laps:
        ranked_cars.append(car)

    return ranked_cars

def get_players_by_most_playtime():
    '''Returns players from most playtime to least'''

    def sort(time_player_pair):
        return list(time_player_pair.keys())[0]

    no_time = []
    ranked_time = []

    for player in get_all_players():
        time = get_player_playtime(player)
        if time == 0:
            no_time.append(player)
        else:
            ranked_time.append({time:player})

    ranked_time.sort(key=sort, reverse=True)

    sorted_players = []

    for time in ranked_time:
        sorted_players.append(list(time.values())[0])
    
    for car in no_time:
        sorted_players.append(car)

    return sorted_players

def get_race_results():
    '''Returns the race results'''

    dao = Dao("laps.json")
    results = dao.get_dataframe()

    race_results = []

    if results.shape[0] > 0:
        race_laps = results[results.session == "Race"]

        for i in range(race_laps.shape[0]):
            
            lap_dict = race_laps.iloc[i].to_dict()

            lap = LapData(json_lap_data = lap_dict)
            race_results.append(lap)

    return race_results

def get_players_by_fastest_lap():
    
    def sort(time_player_pair):
        return list(time_player_pair.keys())[0]

    ranked = []
    no_time = []
    players = get_all_players()

    for player in players:
        time = get_player_fastest_lap(player)
        if time:
            time = time.laptime
            ranked.append({time:player})

        else:
            no_time.append(player)

    
    ranked.sort(key=sort)

    sorted = []

    for time in ranked:
        sorted.append(list(time.values())[0])
    for player in no_time:
        sorted.append(player)

    return sorted




'''TESTS'''
if __name__ == "__main__":
    #print(get_player_fastest_lap(76561198249901871))
    #print(get_car_fastest_lap("nissan_300zx"))
    #print(get_player_fastest_lap_in_car(76561198249901870, "bksy_nissan_skyline_r34_z_tune"))
    #print(get_most_recent_lap())
    #print(get_average_laptime())
    #print(get_all_players())
    #print(get_player_playtime_in_car(76561198249901870, "bksy_nissan_skyline_r34_z_tune"))
    #print(get_car_playtime("bksy_nissan_skyline_r34_z_tune"))
    #print(get_all_cars())
    #print(get_race_results())
    #print(get_all_cars())

    print(get_players_by_fastest_lap())