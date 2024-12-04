from flask import request
from flask import render_template

def login():
    # curl "http://127.0.0.1:5000"   
    print(f"request.url={request.url}")
    return render_template('login.html')