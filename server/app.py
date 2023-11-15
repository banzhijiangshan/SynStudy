from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_bcrypt import Bcrypt

import json
import sqlite3

from database import insert_data, fetch_pw

from utils import process_register_data, process_login_data

app = Flask(__name__)
CORS(app)

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    pass

@app.route('/register', methods=['POST',])
def register():
    raw_data = request.get_data()
    print(raw_data)
    processed_data = process_register_data(raw_data)
    # now hash the raw password
    processed_data['password'] = bcrypt.generate_password_hash(processed_data['password'])
    try:
        insert_data(processed_data)
    except sqlite3.IntegrityError:
        return jsonify(code=409, message="Username already exists!")

    return jsonify(code=200, message="Register successful")

@app.route('/login', methods=['POST',])
def login():
    raw_data = request.get_data()
    print(type(raw_data), raw_data)
    processed_data = process_login_data(raw_data)
    username = processed_data["name"]
    password = processed_data["password"]
    correct_pwd = fetch_pw(username)
    if correct_pwd == None:
        return jsonify(code=401, message="Username not exists!")
    elif not bcrypt.check_password_hash(correct_pwd, password):
        return jsonify(code=401, message="Incorrect password!")
    else:
        return jsonify(code=200, message="Login successful")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5001')