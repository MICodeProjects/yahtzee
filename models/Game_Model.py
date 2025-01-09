# Maya Inal ^-^

import sqlite3
import random
import re
import datetime

class Game:
    def __init__(self, db_name, table_name):
        self.db_name =  db_name
        self.max_safe_id = 9007199254740991 #maximun safe Javascript integer
        self.table_name = table_name
        self.allowed_name_chars = "^[A-Za-z0-9_-]*$"

    
    def initialize_table(self):
        db_connection = sqlite3.connect(self.db_name)
        cursor = db_connection.cursor()
        schema=f"""
                CREATE TABLE {self.table_name} (
                    id INTEGER PRIMARY KEY UNIQUE,
                    name TEXT UNIQUE,
                    created TIMESTAMP,
                    finished TIMESTAMP
                );
                """
        cursor.execute(f"DROP TABLE IF EXISTS {self.table_name};")
        results=cursor.execute(schema)
        db_connection.close()
    
    def exists(self, name):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            # code here

            if self.get(game_name=name)["status"]=="success":
                return {"status":"success", "data":True}
            elif self.get(game_name=name)["data"]=="Game does not exist.":
                return {"status":"success", "data":False}
            else:
                return {"status":"error", "data":self.get(game_name=name)["data"]}
                

        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    def create(self, game_info):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            
            #name check!
            if self.exists(game_info["name"])["data"]==True:
                return {"status":"error", "data":"Game name already exists"}
            #add checks for characters
            if bool(re.match(self.allowed_name_chars, game_info["name"]))==False:
                return {"status":"error", "data":"Invalid characters in name"}

            # check to see if id already exists!!
            game_id = random.randint(0, self.max_safe_id)

            while True:
                exists=self.exists(game_id)
                
                if exists["data"]==False:
                    break
                elif exists["status"]=='error':
                    break
                else:
                    game_id = random.randint(0,self.max_safe_id)
            
            time=str(datetime.datetime.now())
            # created: 'August 19, 2024 23:15:30',

            game_data = (game_id, game_info["name"], time,time)
            #are you sure you have all data in the correct format?
            cursor.execute(f"INSERT INTO {self.table_name} VALUES (?, ?, ?, ?);", game_data)
            db_connection.commit()
            
            

            return {"status": "success",
                    "data": self.to_dict(game_data)
                    } 
        
        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        
        finally:
            db_connection.close()
    
    def get(self, game_name=None, id=None): # don't pass in name or id --> has a value of none, but can still work w only one value 
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            # Insert your code here
            # only using the value that is present
            if id != None:
                game=cursor.execute(f'''SELECT * FROM {self.table_name} WHERE id="{id}";''').fetchone()

            elif game_name !=None:
                game=cursor.execute(f'''SELECT * FROM {self.table_name} WHERE name="{game_name}";''').fetchone()
            else:
                return {"status":"error",
                    "data":"No id or name entered."}
            if game==None:
                return {"status":"error", "data":"Game does not exist."}

            return {"status":"success", "data":self.to_dict(game)}
        

        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()
    
    def get_all(self): # todo
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            games = cursor.execute(f"SELECT * FROM {self.table_name};")
            game_ref = games.fetchall()
            game_list=[]
            for game in game_ref:
                game_list.append(self.to_dict(game))

            return {"status":"success","data":game_list}
        
        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    def update(self, game_info): 
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            if self.get(id=game_info["id"])["data"]=="Game does not exist.":
                return {"status":"error","data":"Game does not exist."}
            print(f"exists?: {self.get(id=game_info['id'])}")

            #name check
            if bool(re.match(self.allowed_name_chars, game_info["name"]))==False: # check if name is valid
                return {"status":"error", "data":"Invalid name entered."}
            if self.exists(game_info["name"])["data"]==True and self.get(game_name=game_info["name"])["data"]["id"] !=game_info["id"]: # check if name exists
                return {"status":"error", "data":f"Name already exists."}
            cursor.execute(f'''UPDATE {self.table_name} SET name="{game_info['name']}" WHERE id={game_info['id']};''')
            db_connection.commit()
            cursor.execute(f'''UPDATE {self.table_name} SET finished="{game_info['finished']}" WHERE id={game_info['id']};''')
            db_connection.commit()

            return {"status":"success", "data":self.get(id=game_info['id'])["data"]}

        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    def remove(self, name): 
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            if self.exists(name)["data"]==False:
                return {"status":"error", "data":'Game does not exist.'}

            game=self.get(game_name=name)["data"]
            cursor.execute(f'''DELETE FROM {self.table_name} WHERE name="{name}";''')
            db_connection.commit()
            return {"status":"success", "data":game}


        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    def is_finished(self, name):
        try:
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            game=self.get(game_name=name)
            if game["status"]=="error":
                return {"status":"error", "data":str(game["data"])}
            #time=f"{time_unfiltered.strftime('%b')} {time_unfiltered.strftime('%d')}, {time_unfiltered.strftime('%G')} {time_unfiltered.strftime('%X')}"
            #'2024-11-15 13:45:52.740726'
            # created: 'August 19, 2024 23:15:30',
            print(game["data"]["created"], game["data"]["finished"])
            return {"status":"success", "data":str(game["data"]["created"])!=str(game["data"]["finished"])}
                
        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        
        finally:
            db_connection.close()

    def to_dict(self, game_tuple):
        '''Utility function which converts the tuple returned from a SQLlite3 database
           into a Python dictionary. So you send it in json format.
        '''
        game_dict={}
        if game_tuple:
            game_dict["id"]=game_tuple[0]
            game_dict["name"]=game_tuple[1]
            game_dict["created"]=str(game_tuple[2])
            game_dict["finished"]=str(game_tuple[3])

        return game_dict

if __name__ == '__main__':
    import os
    print("Current working directory:", os.getcwd())
    DB_location=f"{os.getcwd()}/models/yahtzeeDB.db"

    table_name = "games"
    
    Games = Game(DB_location, table_name) 
    Games.initialize_table()
    games=[{"name":"bobby"}, {"name":"richard"}]
    
    for game in games:
        Games.create(game)
    print(Games.update({"name":"richard", "id":Games.get(game_name="richard")["data"]["id"]}))
    #print(Games.is_finished("robbby"))
 
 #Games.get(game_name="bobby")["data"]["id"]
    

