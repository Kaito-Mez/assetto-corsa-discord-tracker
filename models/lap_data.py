import json

class LapData:
    '''Lap data info class'''
    
    def __init__(self, json_lap, session_data) -> None:
        lap_data = json_lap

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
        
    def __str__(self):
        '''Outputs this lapdata as a serialized json style string'''
        
        self_dict = {
            "player":self.player, 
            "guid":self.guid,
            "laptime":self.laptime,
            "car":self.car,
            "car_id":self.car_id,

        }
        return json.dumps(self_dict, indent=4)


    def to_json(self):
        '''Outputs this lapdata as a serialized json object'''
        
        self_dict = {
            "player":self.player, 
            "guid":self.guid,
            "laptime":self.laptime,
            "car":self.car,
            "car_id":self.car_id,

        }
        return self_dict
