import json

class RaceData:
    '''Race info dataclass'''
    def __init__(self, json_race = None) -> None:
        if json_race is not None:
            results = json_race["Result"]
            self.guids = []
            self.players = []
            self.cars = []
            self.laptimes = []
            for result in results:
                player = result["DriverName"]
                if player != "":
                    self.players.append(player)
                    self.guids.append(result["DriverGuid"])
                    self.cars.append(result["CarModel"])
                    self.laptimes.append(result["TotalTime"])

   
    def __str__(self):
        '''Output this racedata as a json style string'''
        self_dict = {
            "players":self.players,
            "cars":self.cars,
            "laptimes":self.laptimes
        }
        return json.dumps(self_dict, indent=4)

    def to_json(self):
        '''Output this racedata as a json style object'''
        self_json = []

        for i in range(len(self.players)):
            self_json.append({"player":self.players[i], "car":self.cars[i], "guid":self.guids[i], "laptime":self.laptimes[i]})

        return self_json