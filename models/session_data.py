import json

class SessionData:

    def __init__(self, start_time, json_data) -> None:
        
        session_data = json_data

        self.start_time = start_time
        self.end_time = None

        self.session_time = None
        self.player = None
        self.guid = None
        self.car = None
        self.car_id = session_data["car_id"]


    def session_end(self, end_time, json_data):
        self.end_time = end_time

        self.player = json_data["driver_name"]
        self.guid = json_data["driver_guid"]
        self.car = json_data["car_model"]
        self.session_time = (self.end_time - self.start_time).total_seconds()

    def to_json(self):
        self_dict = {
            "player":self.player, 
            "guid":self.guid,
            "session_time":self.session_time,
            "car":self.car,
            "car_id":self.car_id,

        }
        return json.dumps(self_dict, indent=4)