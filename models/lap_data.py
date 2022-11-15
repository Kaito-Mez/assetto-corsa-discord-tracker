import json

class LapData:
    '''Lap data info class'''
    
    def __init__(self, **kwargs) -> None:
        '''Takes either `json_lap_data` or `json_lap`, `session_data` and `session_type`'''

        self.player = ""
        '''Player's name'''
        self.guid = ""
        '''Player's Steam GUID'''
        self.car = ""
        '''Player's car name'''
        self.car_id = -1
        '''Player's car id'''
        #time in ms
        self.laptime = -1
        '''Laptime (milliseconds)'''
        self.session = ""
        '''What type of session it was'''

        json_lap_data = kwargs.get("json_lap_data")

        if json_lap_data is None:
            lap_data = kwargs.get("json_lap")
            session_data = kwargs.get("session_data")
            session_type = kwargs.get("session_type")

            self.player = session_data.player
            self.guid = session_data.guid
            self.car = session_data.car
            self.car_id = session_data.car_id
            self.laptime = lap_data["laptime"]
            self.session = session_type[0]
        else:
            self.player = json_lap_data["player"]
            self.guid = json_lap_data["guid"]
            self.car = json_lap_data["car"]
            self.car_id = json_lap_data["car_id"]
            self.laptime = json_lap_data["laptime"]
            self.session = json_lap_data["session"]
        
        
    def __str__(self):
        '''Outputs this lapdata as a = json style string'''
        self_dict = {
            "player":self.player, 
            "guid":int(self.guid),
            "laptime":int(self.laptime),
            "car":self.car,
            "car_id":int(self.car_id),

        }
        return json.dumps(self_dict, indent=4)


    def to_json(self):
        '''Outputs this lapdata as a json style object'''
        
        self_dict = {
            "player":self.player, 
            "guid":self.guid,
            "laptime":self.laptime,
            "car":self.car,
            "car_id":self.car_id,
            "session":self.session
        }
        return self_dict
