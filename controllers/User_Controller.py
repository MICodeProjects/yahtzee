from flask import jsonify
from flask import request

from models import FruitModel
Fruit_DB_location = './models/data.json'
Fruit = FruitModel.Fruit_Model(Fruit_DB_location)

def fruit():
    print(f"request.method= {request.method} request.url={request.url}")
    print(f"request.url={request.query_string}")
    print(f"request.url={request.args.get('name')}") #GET request & query string
    print(f"request.url={request.form.get('name')}") #POST request & form body

    # curl "http://127.0.0.1:5000/fruit/"
    if request.method == 'GET':
        return jsonify(Fruit.get_all_fruit())
    
    #curl -X POST -H "Content-type: application/json" -d '{ "name" : "tomato", "url":"https://en.wikipedia.org/wiki/Tomato"}' "http://127.0.0.1:5000/fruit/new"
    elif request.method == 'POST':
        return jsonify(Fruit.create_fruit(request.form))


def single_fruit(fruit_name):
    print(f"request.url={request.url}")
    
    if request.method == 'GET':
        # curl "http://127.0.0.1:5000/fruit/apples"
        all_fruit = Fruit.get_all_fruit()
        if fruit_name in all_fruit:
            fruit = {fruit_name: all_fruit[fruit_name]}
            return jsonify(fruit)
        else:
            return {}