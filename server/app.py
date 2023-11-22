import os
from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask import url_for

from werkzeug.utils import secure_filename

import json
import sqlite3

import utils, database


app = Flask(__name__)
app.secret_key = 'a_random_key'

CORS(app)

bcrypt = Bcrypt(app)


@app.route('/')
def index():
    pass

@app.route('/register', methods=['POST',])
def register():
    raw_data = request.get_data()
    print(raw_data)
    processed_data = utils.process_data(raw_data)
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
    processed_data = utils.process_data(raw_data)
    name = processed_data["name"]
    password = processed_data["password"]
    correct_pwd, id = database.fetch_pw_and_id(name)
    if correct_pwd == None:
        return jsonify(code=401, message="User not exists!")
    elif not bcrypt.check_password_hash(correct_pwd, password):
        return jsonify(code=401, message="Incorrect password!")
    else:
        session['user_id'] = int(id)
        return jsonify(code=200, message="Login successful")

@app.route('/logout', methods=['POST',])
def logout():
    session.pop('user_id', None)
    return jsonify(code=200, message="Logout successful")
    
@app.route('/generateStudentId', methods=['GET',])
def get_new_id():
    max_cur_id = database.fetch_cur_cnt()
    new_id = max_cur_id + 10001
    return jsonify(code=200, message="Get new id successful", studentId=new_id)

@app.route('/getStudentName', methods=['GET',])
def get_name_by_id():
    id = session.get('user_id')
    user_info = database.fetch_user_info(id)
    name = user_info['username']
    if name == None:
        return jsonify(code=401, message="id error")
    else:
        return jsonify(code=200, message="Get name successful", name=name)

@app.route('/getUserInfo', methods=['GET',])
def get_user_info():
    id = session.get('user_id')
    user_info = database.fetch_user_info(id)
    user_info['id'] = id + 10000
    print(type(user_info))
    # remove password from dict user_info
    user_info.pop('password', None)
    print(user_info)
    if user_info['image'] == None:
        image_url = None
    else:
        image_url = url_for('static', filename=user_info['image'])
    #user_info['image'] = 'http://localhost:5001/' + user_info['image']
    user_info['image'] = image_url
    print(user_info['image'])
    if user_info == None:
        return jsonify(code=401, message="id error")
    else:
        return jsonify(code=200, message="Get user info successful", userInfo=user_info)
    
@app.route('/updateUserInfo', methods=['POST',])
def update_user_info():
    raw_data = request.get_data()
    print(raw_data)
    processed_data = utils.process_data(raw_data)
    id = session.get('user_id')
    try:
        database.update_user_info(id, processed_data)
    except sqlite3.IntegrityError:
        return jsonify(code=409, message="Username or email already exists!")
    return jsonify(code=200, message="Update user info successful")

@app.route('/uploadAvatar', methods=['POST',])
def upload_avatar():
    # Check if the request has the file part
    print(request.files)
    if 'file' not in request.files:
        return jsonify(code=400, message="No file part")

    file = request.files['file']
    print(type(file))
    print(file)


    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    print(file.filename)
    if file.filename == '':
        return jsonify(code=400, message="No selected file")

    if file:
        filename = secure_filename(file.filename)
        save_path = os.path.join('static/user_pics', filename)
        # save save_path to database
        id = session.get('user_id')
        database.update_user_info(id, {'image': save_path[7:]})

        file.save(save_path)
        return jsonify(code=200, message="Upload avatar successful")

@app.route('/classRoom', methods=['POST',])
def enter_classroom():
    raw_data = request.get_data()
    print(raw_data)
    processed_data = utils.process_data(raw_data)
    subject = processed_data['subject']
    id = session.get('user_id')
    classroom_id = database.get_classroom_id(subject)
    # set session classroom_id
    session['classroom_id'] = classroom_id
    if classroom_id == None:
        return jsonify(code=401, message="Classroom not exists!")
    else:
        try:
            database.enter_classroom(id, classroom_id)
        except sqlite3.IntegrityError:
            return jsonify(code=409, message="Classroom full!")
        return jsonify(code=200, message="Enter classroom successful")
    
@app.route('/exitClassRoom', methods=['POST',])
def leave_classroom():
    id = session.get('user_id')
    classroom_id = session.get('classroom_id')
    # pop session classroom_id
    session.pop('classroom_id', None)
    if classroom_id == None:
        return jsonify(code=401, message="Classroom not set!")
    else:
        try:
            database.leave_classroom(id, classroom_id)
        except sqlite3.IntegrityError:
            return jsonify(code=409, message="Classroom already empty, please check for error!")
        return jsonify(code=200, message="Leave classroom successful")
   
@app.route('/getStudyInfo', methods=['GET',])
def get_study_info():
    # get study time using id
    id = session.get('user_id')
    hours, mins = database.get_study_time(id)
    # get online_num using classroom_id
    classroom_id = session.get('classroom_id')
    online_num = database.get_online_num(classroom_id)

    return jsonify(code = 200, message='Get success', studyInfo={'hour':hours, 'minute':mins, 'studytogether':online_num})

@app.route('/timeIncrease', methods=['POST',])
def time_increase():
    raw_data = request.get_data()
    print(raw_data)
    processed_data = utils.process_data(raw_data)
    id = session.get('user_id')
    mins = processed_data['min']

    database.increase_study_time(id, mins)
    return jsonify(code=200, message="Increase study time successful")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5001')