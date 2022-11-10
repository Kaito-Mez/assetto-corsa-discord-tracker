import json

class SessionData:
    '''Player play session info dataclass'''

    def __init__(self, start_time, json_data) -> None:
        
        session_data = json_data

        self.start_time = start_time
        '''Session start time'''
        self.end_time = None
        '''Session end time'''
        self.session_time = None
        '''Total duration of the session'''
        self.player = None
        '''Players name'''
        self.guid = None
        '''Player's steam GUID'''
        self.car = None
        '''Player's car name'''
        self.car_id = session_data["car_id"]
        '''Player's car ID'''

    def __str__(self):
        '''Outputs this sessiondata as a json style string'''
        self_dict = {
            "player":self.player, 
            "guid":self.guid,
            "session_time":self.session_time,
            "car":self.car,
            "car_id":self.car_id,

        }
        return json.dumps(self_dict, indent=4)

    def update_car_info(self, json_data):
        '''Set data once the car has been queried'''
        self.player = json_data["driver_name"]
        self.guid = json_data["driver_guid"]
        self.car = json_data["car_model"]

    def session_end(self, end_time):
        '''Add the end time and calc total session time'''
        self.end_time = end_time

        self.session_time = (self.end_time - self.start_time).total_seconds()



    def to_json(self):
        '''Ouputs this sessiondata as a serialized json object'''
        self_dict = {
            "player":self.player, 
            "guid":self.guid,
            "session_time":self.session_time,
            "car":self.car,
            "car_id":self.car_id,

        }
        return self_dict