import json

class PlayerData:

    def __init__(self, json_player = None) -> None:
        if json_player is not None:
            self.name = json_player["name"]
            self.guid = json_player["guid"]
            self.playtime = json_player["playtime"]
            self.best_time = json_player["best_time"]
            self.best_car = json_player["best_car"]
            self.car_stats = json_player["car_stats"]

    def setup(self, name, guid):
        self.name = name
        self.guid = guid

    def add_session_time(self, session_time, car):
        self.playtime += session_time
        self.car_stats[car] += session_time

    def to_json(self):
        self_dict = {
            "name":self.name, 
            "guid":self.guid,
            "playtime":self.playtime,
            "best_time":self.best_time,
            "best_car":self.best_car,
            "car_stats":self.car_stats
        }
        return json.dumps(self_dict, indent=4)