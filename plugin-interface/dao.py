import json


class Dao:
    '''Data access object for lap data'''

    def __init__(self, filename) -> None:
        self.filepath = "./database/" + filename

    def save(self, json_string):
        '''Saves object to opened file'''

        with open(self.filepath, "r") as f:
            db_data = json.load(f)
            print(type(db_data))
            print(db_data)
            db_data.append(json_string)
            f.close()

        with open(self.filepath, "w") as g:
            json.dump(db_data, g)
            f.close()
    
    def get_json(self):
        '''Returns file as a json string'''
        
        with open(self.filepath, "r") as f:
            db_string = json.loads(f)
            f.close()
        
        return db_string
    