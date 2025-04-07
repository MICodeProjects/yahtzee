# Maya Inal :3

import sqlite3
import random
import json
import re
import datetime

from User_Model import User
from Game_Model import Game


class Scorecard:
    def __init__(self, db_name, scorecard_table_name, user_table_name, game_table_name):
        self.db_name =  db_name
        self.max_safe_id = 9007199254740991 #maximun safe Javascript integer
        self.table_name = scorecard_table_name 
        self.user_table_name = user_table_name
        self.game_table_name = game_table_name



    
    def initialize_table(self):
        db_connection = sqlite3.connect(self.db_name, )
        cursor = db_connection.cursor()
        schema=f"""
                CREATE TABLE {self.table_name} (
                    id INTEGER PRIMARY KEY UNIQUE,
                    game_id INTEGER,
                    user_id INTEGER,
                    categories TEXT,
                    turn_order INTEGER,
                    name TEXT,
                    FOREIGN KEY(game_id) REFERENCES {self.game_table_name}(id) ON DELETE CASCADE,
                    FOREIGN KEY(user_id) REFERENCES {self.user_table_name}(id) ON DELETE CASCADE
                )
                """
        cursor.execute(f"DROP TABLE IF EXISTS {self.table_name};")
        results=cursor.execute(schema)
        db_connection.close()
         
    def create(self, game_id, user_id, name):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            card_id = random.randint(0, self.max_safe_id)
            
            # get game_name and username
            game_name=name.split('|')[0]
            username=name.split('|')[1]


            # check that user does not have a scorecard in this game already
            if username in self.get_all_game_usernames(game_name)["data"]:
                return {"status":"error", "data":"User already in game."}
            
            # check that name does NOT exist
            if self.get(name=name)["data"]=="success":
                return {"status":"error", "data":"Scorecard name already exists"}
            # check that game does not have 4 players already
            players_in_game=len(self.get_all_game_scorecards(game_name)["data"])
            if players_in_game==4:
                return {"status":"error", "data":"Already 4 players in the game."}
            
            # add turn order
            turn_order=players_in_game+1            


            # create unique id
            while True:
                
                if self.get(id=card_id)["data"]=="Scorecard does not exist.":
                    break
                elif self.get(id=card_id)["status"]=="error":
                    return {"status":"error", "data":str(self.get(id=card_id)["data"])}
                else:
                    card_id = random.randint(0,self.max_safe_id)
            
            categories=json.dumps(self.create_blank_score_info())
            game_data = (card_id, game_id, user_id,categories,turn_order,name)
            #are you sure you have all data in the correct format?
            cursor.execute(f"INSERT INTO {self.table_name} VALUES (?, ?, ?, ?, ?, ?);", game_data)
            db_connection.commit()
            
            

            return {"status": "success",
                    "data": self.to_dict(game_data)
                    } 

   
        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    def get(self, name=None, id=None):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            scorecard=None
            cursor = db_connection.cursor()
            if name!=None:
                scorecard=cursor.execute(f'''SELECT * FROM {self.table_name} WHERE name="{name}";''').fetchone()
            elif id!=None:
                scorecard=cursor.execute(f'''SELECT * FROM {self.table_name} WHERE id={id};''').fetchone()
            else:
                return {"status":"error", "data":"No name or id entered."}
            if scorecard==None:
                return {"status":"error", "data":"Scorecard does not exist."}
            return {"status":"success", "data":self.to_dict(scorecard)}

        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()
    
    def get_all(self): 
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            scorecards = cursor.execute(f"SELECT * FROM {self.table_name};")
            scorecard_list=[]
            for scorecard in scorecards.fetchall():
                scorecard_list.append(self.to_dict(scorecard))

            return {"status":"success","data":scorecard_list}


        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()
    
    # given a game_name, which scorecards are playing in it?
    def get_all_game_scorecards(self, game_name:str): 
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            game_scorecards_unfiltered=cursor.execute(f'''SELECT * FROM {self.table_name} INNER JOIN {self.game_table_name} 
                                                          ON {self.table_name}.game_id={self.game_table_name}.id AND {self.game_table_name}.name="{game_name}";''').fetchall()
            
            game_scorecards=[]
            for game_scorecard in game_scorecards_unfiltered:
                if type(game_scorecard) != int: # making sure we don't add ids
                    game_scorecards.append(self.to_dict(game_scorecard))

            
            return {"status":"success", "data":game_scorecards}

        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    # given a game, what are the usernames associated with it?
    def get_all_game_usernames(self, game_name:str): 
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            
            user_ids=cursor.execute(f'''SELECT {self.table_name}.user_id 
                                        FROM {self.table_name} INNER JOIN {self.game_table_name} 
                                        ON {self.table_name}.game_id={self.game_table_name}.id AND {self.game_table_name}.name="{game_name}";''').fetchall()
            
            usernames=[]
            for user_id in user_ids:
                username=cursor.execute(f'''SELECT username
                                            FROM {self.user_table_name} 
                                            WHERE id={user_id[0]};''').fetchone()
                
                usernames.append(username[0])


            
            return {"status":"success", "data":usernames}


        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    # given a username, what game names is it in?
    def get_all_user_game_names(self, username:str): 
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            game_ids=cursor.execute(f'''SELECT {self.table_name}.game_id 
                                        FROM {self.table_name} INNER JOIN {self.user_table_name} 
                                        ON {self.table_name}.user_id={self.user_table_name}.id AND {self.user_table_name}.username="{username}";''').fetchall()
            game_names=[]
            for id in game_ids:
                game_name=cursor.execute(f'''SELECT name FROM {self.game_table_name} WHERE id={id[0]};''').fetchone()
                game_names.append(game_name[0])

            return {"status":"success", "data":game_names}


        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    def update(self, id, name=None, categories=None): 
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            # making sure that id exists
            if self.get(id=id)["data"]=="Scorecard does not exist.":
                return {"status":"error","data":"Scorecard id does not exist."}
            
            
            # if name has a value:
            if name!=None:

                # checking no other scorecard has same name
                if self.get(name=name)["status"]=="success" and self.get(name=name)["data"]["id"]!=id:
                    return {"status":"error","data":"Scorecard name already exists."} # MAY CAUSE ERRORS may need to swtich to a success?
                
                cursor.execute(f'''UPDATE {self.table_name} SET name="{name}" WHERE id={id};''')
                db_connection.commit()

            # if score_info has a value:
            if categories !=None:
                cursor.execute(f'''UPDATE {self.table_name} SET categories='{json.dumps(categories)}' WHERE id={id};''')
                db_connection.commit()
                
            return {"status":"success", "data":self.get(id=id)["data"]}

        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    def remove(self, id): 
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            # making sure that id exists
            if self.get(id=id)["data"]=="Scorecard does not exist.":
                return {"status":"error","data":"Scorecard id does not exist."}
            
            removed_scorecard=self.get(id=id)["data"]

            cursor.execute(f'''DELETE FROM {self.table_name} WHERE id={id};''')          
            db_connection.commit()  
            return {"status":"success", "data":removed_scorecard}

        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()
    
    def to_dict(self, card_tuple):
        game_dict={}
        if card_tuple:
            game_dict["id"]=card_tuple[0]
            game_dict["game_id"]=card_tuple[1]
            game_dict["user_id"]=card_tuple[2]
            game_dict["categories"]=json.loads(card_tuple[3])
            game_dict["turn_order"]=card_tuple[4]
            game_dict["name"]=card_tuple[5]
        return game_dict
    
    def create_blank_score_info(self):
        return {
            "dice_rolls":0,
            "upper":{
                "ones":-1,
                "twos":-1,
                "threes":-1,
                "fours":-1,
                "fives":-1,
                "sixes":-1
            },
            "lower":{
                "three_of_a_kind":-1,
                "four_of_a_kind":-1,
                "full_house":-1,
                "small_straight":-1,
                "large_straight":-1,
                "yahtzee":-1,
                "chance":-1
            }
        }

    def tally_score(self, score_info):
        total_score = 0
        for value in list(score_info["upper"].values()):
            if value != -1:
                total_score+=value

        if total_score>63:
            total_score+=35
        
        for value in list(score_info["lower"].values()):
            if value != -1:
                total_score+=value
        
        return total_score
    
    
    def get_high_scores_list(self, username):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            all_games=self.get_all_user_game_names(username)

            # check 4 errors or if its empty
            if all_games["status"]=="error" or all_games["data"]==[]:
                return all_games
            
            
            all_scorecards=[]
            
            for game_name in all_games["data"]:
                
                game_scorecard=cursor.execute(f'''SELECT *
                                            FROM {self.table_name} INNER JOIN {self.game_table_name} 
                                            ON {self.table_name}.game_id={self.game_table_name}.id AND {self.game_table_name}.name="{game_name}";''').fetchone()
                all_scorecards.append({"score":self.tally_score(self.to_dict(game_scorecard)["categories"]), "game_name":game_name})
                
                
            # sort list of dictionaries by score (high to low)
            return {"status":"success", "data":sorted(all_scorecards, key=lambda d:d["score"])[::-1]}
        
        except sqlite3.Error as error:
            return {"status":"error",
                        "data":error}
        finally:
            db_connection.close()
    
    def get_game_turn_order(self, game_name):
        turn_order = {}
        players = self.get_all_game_scorecards(game_name)["data"]
        for player in players:
            turn_order[player["turn_order"]] =player["name"].split("|")[1]

        return {"status":"success", "data":turn_order}
        
   

if __name__ == '__main__':
    import os
    #print("Current working directory:", os.getcwd())
    DB_location=f"{os.getcwd()}/models/yahtzeeDB.db"
    #print("location", DB_location)
    Users = User(DB_location, "users")
    Users.initialize_table()
    users=[{"email":"cookie.monster@trinityschoolnyc.org",
                    "username":"cookieM",
                    "password":"123TriniT"},
                    {"email":"justin.gohde@trinityschoolnyc.org",
                    "username":"justingohde",
                    "password":"123TriniT"}]
    
    for user in users:
        Users.create(user)
    Games = Game(DB_location, "games")
    Games.initialize_table()
    games=[{"name":"game1"}, {"name":"game2"}, {"name":"game3"}]
    for game in games:
        Games.create(game)

    Scorecards = Scorecard(DB_location, "scorecards", "users", "games")
    Scorecards.initialize_table()
    Scorecards.create(Games.get(game_name="game1")["data"]["id"], Users.get(username="justingohde")["data"]["id"], "game1|justingohde")
    Scorecards.create(Games.get(game_name="game2")["data"]["id"], Users.get(username="justingohde")["data"]["id"], "game2|justingohde")
    Scorecards.create(Games.get(game_name="game3")["data"]["id"], Users.get(username="justingohde")["data"]["id"], "game3|justingohde")
    # print(Scorecards.get_chronological_games("justingohde"))

    