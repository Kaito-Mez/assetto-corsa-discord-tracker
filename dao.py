import json
import pandas as pd



class Dao:
    '''Data access object for lap data'''

    def __init__(self, filename) -> None:
        self.filepath = "./database/" + filename

    def save(self, json_data):
        '''Saves object to opened file'''
        print(self.filepath)
        with open(self.filepath, "r") as f:
            db_string = f.read()
            db_data = json.loads(db_string)
            db_data.append(json_data)
        
        with open(self.filepath, "w+") as f:
            json.dump(db_data, f, indent=4)
    
    def get_json(self):
        '''Returns file as a json string'''
        
        with open(self.filepath, "r") as f:
            db_string = json.loads(f)
        
        return db_string

    def get_dataframe(self):
        df = pd.read_json(self.filepath, dtype={"guid":"int64"})
        return df
    