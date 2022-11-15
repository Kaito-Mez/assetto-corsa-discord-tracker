import json

class LapData:
    '''Lap data info class'''
    
    def __init__(self, json_lap, session_data, session_type, **kwargs) -> None:


        lap_data = kwargs.get("json_lap")
        session_data = kwargs.get("session_data")
        session_type = kwargs.get("session_type")

        self.player = session_data.player
        '''Player's name'''
        self.guid = session_data.guid
        '''Player's Steam GUID'''
        self.car = session_data.car
        '''Player's car name'''
        self.car_id = session_data.car_id
        '''Player's car id'''
        #time in ms
        self.laptime = lap_data["laptime"]
        '''Laptime (milliseconds)'''

        self.session = session_type[0]
        '''What type of session it was'''
        
    def __str__(self):
        '''Outputs this lapdata as a = json style string'''
        
        self_dict = {
            "player":self.player, 
            "guid":self.guid,
            "laptime":self.laptime,
            "car":self.car,
            "car_id":self.car_id,

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
