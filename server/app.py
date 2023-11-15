from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_bcrypt import Bcrypt

import json
import sqlite3

import utils, database


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
    processed_data = utils.process_register_data(raw_data)
    # now hash the raw password
    processed_data['password'] = bcrypt.generate_password_hash(processed_data['password'])
    try:
        database.insert_register_data(processed_data)
    except sqlite3.IntegrityError:
        return jsonify(code=409, message="Username already exists!")

    return jsonify(code=200, message="Register successful")

@app.route('/login', methods=['POST',])
def login():
    raw_data = request.get_data()
    print(type(raw_data), raw_data)
    processed_data = utils.process_login_data(raw_data)
    id = processed_data["name"]
    password = processed_data["password"]
    correct_pwd = database.fetch_pw(id)
    if correct_pwd == None:
        return jsonify(code=401, message="User not exists!")
    elif not bcrypt.check_password_hash(correct_pwd, password):
        return jsonify(code=401, message="Incorrect password!")
    else:
        return jsonify(code=200, message="Login successful")
    
@app.route('/generateStudentId', methods=['GET',])
def get_new_id():
    max_cur_id = database.fetch_cur_cnt()
    new_id = max_cur_id + 10001
    return jsonify(code=200, message="Get new id successful", data={'studentId':new_id})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5001')