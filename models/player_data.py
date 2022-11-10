import json

class PlayerData:
    '''Player info dataclass'''
    def __init__(self, json_player = None) -> None:
        if json_player is not None:
            self.name = json_player["name"]
            '''Player's name'''
            self.guid = json_player["guid"]
            '''Player's Steam GUID'''
            self.playtime = json_player["playtime"]
            '''Total playtime on server (seconds)'''
            self.best_time = json_player["best_time"]
            '''Fastest Laptime'''
            self.best_car = json_player["best_car"]
            '''Car that the fastest laptime was achieved in'''
            self.car_stats = json_player["car_stats"]
            '''Player stats with all cars'''
   
    def __str__(self):
        '''Output this playerdata as a json style string'''
        self_dict = {
            "name":self.name, 
            "guid":self.guid,
            "playtime":self.playtime,
            "best_time":self.best_time,
            "best_car":self.best_car,
            "car_stats":self.car_stats
        }
        return json.dumps(self_dict, indent=4)

    def setup(self, name, guid):
        '''Set name and guid of player'''
        self.name = name
        self.guid = guid

    def add_session_time(self, session_time, car):
        '''Add the data from a session'''
        self.playtime += session_time
        self.car_stats[car] += session_time



    def to_json(self):
        '''Output this playerdata as a serialized json object'''
        self_dict = {
            "name":self.name, 
            "guid":self.guid,
            "playtime":self.playtime,
            "best_time":self.best_time,
            "best_car":self.best_car,
            "car_stats":self.car_stats
        }
        return self_dict