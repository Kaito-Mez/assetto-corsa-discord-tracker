from models.lap_data import LapData
from dao import Dao

def get_player_fastest_lap(guid) -> LapData or None:
    '''Gets the fasest lap of specified player'''

    fastest_lap = None

    dao = Dao("laps.json")
    all_laps = dao.get_dataframe()
    all_laps = all_laps[all_laps.session != "Practice"]
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
    all_laps = all_laps[all_laps.session != "Practice"]
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
    all_laps = all_laps[all_laps.session != "Practice"]
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

    dao = Dao("laps.json")
    
    all_laps = dao.get_dataframe()

    try:
        most_recent = all_laps.iloc[-1].to_dict()
    except IndexError as e:
        pass
    
    lap = None

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

    all_players = all_laps.guid.unique()
    
    return list(all_players)

def get_player_playtime(guid):
    '''Gets a player's total playtime on the server in seconds'''

    dao = Dao("sessions.json")
    all_sessions = dao.get_dataframe()
    player_sessions = all_sessions[all_sessions.guid == guid]

    total_playtime = player_sessions.session_time.sum()

    return total_playtime

def get_player_playtime_in_car(guid, car):
    '''Gets a player's total playtime on the server in a specific car'''

    dao = Dao("sessions.json")
    all_sessions = dao.get_dataframe()
    player_sessions = all_sessions[all_sessions.guid == guid]
    car_sessions = player_sessions[player_sessions.car == car]

    return car_sessions.session_time.sum()

def get_car_playtime(car):
    '''Gets the total playtime of a car regardless of player'''
    dao = Dao("sessions.json")
    all_sessions = dao.get_dataframe()
    car_sessions = all_sessions[all_sessions.car == car]

    return car_sessions.session_time.sum()

def get_all_cars():
    '''Returns all car names'''

    dao = Dao("laps.json")

    all_laps = dao.get_dataframe()

    all_cars =  all_laps.car.unique()

    return list(all_cars)

'''TESTS'''
if __name__ == "__main__":
    #print(get_player_fastest_lap(76561198249901871))
    #print(get_car_fastest_lap("pschd_honda_integra_dc2_typer_1998"))
    print(get_player_fastest_lap_in_car(76561198249901870, "bksy_nissan_skyline_r34_z_tune"))
    #print(get_most_recent_lap())
    #print(get_average_laptime())
    #print(get_all_players())
    print(get_player_playtime_in_car(76561198249901870, "bksy_nissan_skyline_r34_z_tune"))
    print(get_car_playtime("bksy_nissan_skyline_r34_z_tune"))