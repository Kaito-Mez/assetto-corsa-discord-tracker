import json


class Dao:
    '''Data access object for lap data'''

    def __init__(self, filename) -> None:
        self.filepath = "database/" + filename

    def save(self, json_string):
        '''Saves object to opened file'''
        print(self.filepath)
        with open(self.filepath, "r+") as f:
            db_string = f.read()
            db_data = json.loads(db_string)
        
    
            print(type(db_data))
            print(db_data)
            db_data.append(json_string)



        with open(self.filepath, "w") as f:
            json.dump(db_data, f)
            f.write("Test")
            print("here")
            f.close()
    
    def get_json(self):
        '''Returns file as a json string'''
        
        with open(self.filepath, "r") as f:
            db_string = json.loads(f)
            f.close()
        
        return db_string
    