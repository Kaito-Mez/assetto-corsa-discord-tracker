import json

class LapData:
    
    def __init__(self, json_lap, json_car_info) -> None:
        lap_data = json_lap
        car_data = json_car_info

        self.player = car_data["driver_name"]
        self.player_id = car_data["driver_guid"]
        self.car = car_data["car_model"]
        self.car_id = car_data["car_id"]
        #time in ms
        self.time = lap_data["laptime"]
        


    def to_json(self):
        return json.dumps(self, indent=4)
