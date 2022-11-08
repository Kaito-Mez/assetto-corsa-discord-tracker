import json

class LapData:
    
    def __init__(self, json_lap, session_data) -> None:
        lap_data = json_lap

        self.player = session_data.player
        self.guid = session_data.guid
        self.car = session_data.car
        self.car_id = session_data.car_id
        #time in ms
        self.laptime = lap_data["laptime"]
        


    def to_json(self):
        self_dict = {
            "player":self.player, 
            "guid":self.guid,
            "laptime":self.laptime,
            "car":self.car,
            "car_id":self.car_id,

        }
        return json.dumps(self_dict, indent=4)
