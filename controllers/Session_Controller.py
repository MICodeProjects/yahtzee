from flask import request
from flask import render_template

def login():
    # curl "http://127.0.0.1:5000"   
    print(f"request.url={request.url}")
    username=request.args.get("username")
    password=request.args.get("password")

    return render_template('user_games.html', username=username, password=password)

def index():
    # can send info through route, query string, body
    return render_template('login.html')





