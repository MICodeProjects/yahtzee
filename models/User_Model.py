# Maya Inal ^-^

import sqlite3
import random
import re

class User:
    def __init__(self, db_name, table_name):
        self.db_name =  db_name
        self.max_safe_id = 9007199254740991 #maximun safe Javascript integer
        self.table_name = table_name
        self.allowed_username_chars = "^[A-Za-z0-9_-]*$"
    
    def initialize_table(self):
        db_connection = sqlite3.connect(self.db_name)
        cursor = db_connection.cursor()
        schema=f"""
                CREATE TABLE {self.table_name} (
                    id INTEGER PRIMARY KEY UNIQUE,
                    email TEXT UNIQUE,
                    username TEXT UNIQUE,
                    password TEXT
                );
                """
        cursor.execute(f"DROP TABLE IF EXISTS {self.table_name};")
        results=cursor.execute(schema)
        db_connection.close()
    
    def exists(self, username=None, id=None):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            # code here
            if id!=None:
                if self.get(id=id)["status"]=="success":
                    return {"status":"success", "data":True}
                elif self.get(id=id)["data"]=="User does not exist.":
                    return {"status":"success", "data":False}
                else:
                    return {"status":"error", "data":self.get(id)["data"]}
            elif username!=None:
                if self.get(username=username)["status"]=="success":
                    return {"status":"success", "data":True}
                elif self.get(username=username)["data"]=="User does not exist.":
                    return {"status":"success", "data":False}
                else:
                    return {"status":"error", "data":self.get(username)["data"]}
                
            return {"status":"error", "data":"No username or id entered"} # might cause errors! may need to change data val

        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    def create(self, user_info):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            users = self.get_all()
            #username check!
            if self.exists(username=user_info["username"])["data"]==True:
                return {"status":"error", "data":"Username already exists"}
            #add checks for characters
            if bool(re.match(self.allowed_username_chars, user_info["username"]))==False:
                return {"status":"error", "data":"Invalid characters in username"}

            # email check!
            for user in users["data"]:
                if user["email"]==user_info["email"]:
                    return {"status":"error", "data":"Email already in use"} 
            if "@" not in user_info["email"] or "." not in user_info["email"] or '"' in user_info["email"]:
                return {"status":"error", "data":"Invalid or missing characters in email"}

            # password check!
            if len(user_info["password"])<8:
                return {"status":"error", "data":"Password too short"}   

            # check to see if id already exists!!
            user_id = random.randint(0, self.max_safe_id)

            while True:
                exists=self.exists(id=user_id)
                
                if exists["data"]==False:
                    break
                elif exists["status"]=='error':
                    break
                else:
                    user_id = random.randint(0,self.max_safe_id)

            
            user_data = (user_id, user_info["email"], user_info["username"], user_info["password"])
            #are you sure you have all data in the correct format?
            cursor.execute(f"INSERT INTO {self.table_name} VALUES (?, ?, ?, ?);", user_data)
            db_connection.commit()
            
            

            return {"status": "success",
                    "data": self.to_dict(user_data)
                    } 
        
        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        
        finally:
            db_connection.close()
    
    def get(self, username=None, id=None): # don't pass in username or id --> has a value of none, but can still work w only one value 
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            # Insert your code here
            # only using the value that is present
            if id != None:
                user=cursor.execute(f'''SELECT * FROM {self.table_name} WHERE id="{id}";''').fetchone()

            elif username !=None:
                user=cursor.execute(f'''SELECT * FROM {self.table_name} WHERE username="{username}";''').fetchone()
            else:
                return {"status":"error",
                    "data":"No id or username entered"}
            if user==None:
                return {"status":"error", "data":"User does not exist."}

            return {"status":"success", "data":self.to_dict(user)}
        

        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()
    
    def get_all(self): # todo
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            users = cursor.execute(f"SELECT * FROM {self.table_name};")
            user_ref = users.fetchall()
            user_list=[]
            for user in user_ref:
                user_list.append(self.to_dict(user))

            return {"status":"success","data":user_list}
        
        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    def update(self, user_info): 
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            if self.exists(id=user_info["id"])["data"]==False:
                return {"status":"error","data":"User does not exist."}

            users=self.get_all()["data"]
            #username check
            if bool(re.match(self.allowed_username_chars, user_info["username"]))==False: # check if username is valid
                return {"status":"error", "data":"Invalid username entered."}
            if self.exists(user_info["username"])["data"]==True and self.get(username=user_info["username"])["data"]["id"] !=user_info["id"]: # check if username exists
                return {"status":"error", "data":f"Username already exists."}
            
            #email check
            if "@" not in user_info["email"] or "." not in user_info["email"] or '"' in user_info["email"]: # check if email is valid
                return {"status":"error", "data":"Invalid characters in email."} 
            for user in users: # check if email in use
                if user["email"]==user_info["email"] and user["id"] != user_info["id"]:
                    return {"status":"error", "data":f"Email already in use. id : {user_info['id']}"}

   

            #password check
            if len(user_info["password"])<8: # is password long enough?
                return {"status":"error", "data":"Password too short"}   

            cursor.execute(f'''UPDATE {self.table_name} 
                           SET username="{user_info['username']}",
                           email="{user_info['email']}",
                           password="{user_info['password']}"
                           WHERE id={user_info['id']};''')
            db_connection.commit()

            return {"status":"success", "data":user_info}

        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    def remove(self, username): 
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            if self.exists(username=username)["data"]==False:
                return {"status":"error", "data":'Username does not exist.'}
            user=self.get(username=username)["data"]
            cursor.execute(f'''DELETE FROM {self.table_name} WHERE username="{username}"''')
            db_connection.commit()
            return {"status":"success", "data":user}


        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()
    
    def to_dict(self, user_tuple):
        '''Utility function which converts the tuple returned from a SQLlite3 database
           into a Python dictionary. So you send it in json format.
        '''
        user_dict={}
        if user_tuple:
            user_dict["id"]=user_tuple[0]
            user_dict["email"]=user_tuple[1]
            user_dict["username"]=user_tuple[2]
            user_dict["password"]=user_tuple[3]
        return user_dict

if __name__ == '__main__':
    import os
    print("Current working directory:", os.getcwd())
    DB_location=f"{os.getcwd()}/yahtzeeDB.db"
    table_name = "users"
    
    Users = User(DB_location, table_name) 
    Users.initialize_table()
    users=[{"email":"cookie.monster@trinityschoolnyc.org",
                    "username":"cookieM",
                    "password":"123TriniT"},
                    {"email":"justin.gohde@trinityschoolnyc.org",
                    "username":"justingohde",
                    "password":"123TriniT"}]
                    # {"email":"zelda@trinityschoolnyc.org",
                    # "username":"princessZ",
                    # "password":"123TriniT"},
                    # {"email":"test.user@trinityschoolnyc.org",
                    # "username":"testuser",
                    # "password":"123TriniT"}
    
    for user in users:
        Users.create(user)
    

    #print(Users.get(username = "justingohde"))
    # print(Users.update({"email":"cookie.sdfsdf@trinityschoolnyc.org",
    #                 "username":"cookffieM",
    #                 "password":"123TffiniT",
    #                 "id":Users.get(username="cookieM")["data"]["id"]}))
    # print(Users.get_all())