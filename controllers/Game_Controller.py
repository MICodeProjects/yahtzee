from flask import jsonify
from flask import request

from models import Game_Model
game_DB_location = 'yahtzeeDB.db'
Game = Game_Model.Game_Model(game_DB_location)

# def games():
#     print(f"request.method= {request.method} request.url={request.url}")
#     print(f"request.url={request.query_string}")
#     print(f"request.url={request.args.get('name')}") #GET request & query string # from name. name=whatever in variable becomes the nameof it
#     print(f"request.url={request.form.get('name')}") #POST request & form body

#     # curl "http://127.0.0.1:5000/fruit/"
#     if request.method == 'GET':
#         return jsonify(Game.get_all_fruit())
    
#     #curl -X POST -H "Content-type: application/json" -d '{ "name" : "tomato", "url":"https://en.wikipedia.org/wiki/Tomato"}' "http://127.0.0.1:5000/fruit/new"
#     elif request.method == 'POST':
#         return jsonify(Game.create(request.form))
    
# def delete_user_from_game(game_name, username):
