from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import sqlite3

from database import insert_data, fetch_data

from utils import process_register_data, process_login_data

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    pass

@app.route('/register', methods=['POST',])
def register():
    raw_data = request.get_data()
    print(raw_data)
    processed_data = process_register_data(raw_data)
    try:
        insert_data(processed_data)
    except sqlite3.IntegrityError:
        return jsonify(code=409, message="Username already exists!"), 409

    return jsonify(code=200, message="Register successful")

@app.route('/login', methods=['POST',])
def login():
    raw_data = request.get_data()
    print(type(raw_data), raw_data)
    processed_data = process_login_data(raw_data)
    if processed_data:
        username = processed_data["username"]
        password = processed_data["password"]
        correct_pwd = fetch_data(username)
        if correct_pwd == None:
            return jsonify(code=401, message="Username not exists!"), 401
        elif correct_pwd != password:
            return jsonify(code=401, message="Incorrect password!"), 401
        else:
            return jsonify(code=200, message="Login successful")
    else:
        return jsonify(code=200, message="Trial successful")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5001')