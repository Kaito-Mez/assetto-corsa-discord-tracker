import json

class PlayerData:

    def __init__(self, json_player) -> None:
        self.name = json_player["name"]
        self.guid = json_player["guid"]
        self.playtime = json_player["playtime"]
        self.best_time = json_player["best_time"]
        self.best_time_car = json_player["best_time_car"]
        self.favourite_car = json_player["favourite_car"]

    def add_session_time(self, session_time):
        self.playtime += session_time

    def to_json(self):
        return json.dumps(self, indent=4)