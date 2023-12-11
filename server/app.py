import os
from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask import url_for

from werkzeug.utils import secure_filename

import json
import sqlite3

import utils
import database


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
    processed_data['password'] = bcrypt.generate_password_hash(
        processed_data['password'])
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
    if correct_pwd is None:
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
    if name is None:
        return jsonify(code=401, message="id error")
    else:
        return jsonify(code=200, message="Get name successful", name=name)



@app.route('/getUserInfo', methods=['GET',])
def get_user_info():
    id = session.get('user_id')
    user_info = database.fetch_user_info(id)
    user_info['id'] = id + 10000
    # print(type(user_info))
    # remove password from dict user_info
    user_info.pop('password', None)
    # print(user_info)
    image_url = url_for('static', \
                        filename=user_info['image'] if user_info['image'] else "user_pics/default.jpg")
    # if user_info['image'] is None:
    #     image_url = None
    # else:
    #     image_url = url_for('static', filename=user_info['image'])
    # user_info['image'] = 'http://localhost:5001/' + user_info['image']
    user_info['image'] = image_url
    # print(user_info['image'])
    if user_info is None:
        return jsonify(code=401, message="id error")
    else:
        return jsonify(code=200,
                       message="Get user info successful",
                       userInfo=user_info)


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
    if classroom_id is None:
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
    if classroom_id is None:
        return jsonify(code=401, message="Classroom not set!")
    else:
        try:
            database.leave_classroom(id, classroom_id)
        except sqlite3.IntegrityError:
            return jsonify(code=409,
                           message="Classroom already empty, \
                            please check for error!")
        return jsonify(code=200, message="Leave classroom successful")




@app.route('/getStudyInfo', methods=['GET',])
def get_study_info():
    # get study time using id
    id = session.get('user_id')
    hours, mins = database.get_study_time(id)
    # get online_num using classroom_id
    classroom_id = session.get('classroom_id')
    online_num = database.get_online_num(classroom_id)

    return jsonify(code=200,
                   message='Get success',
                   studyInfo={
                       'hour': hours,
                       'minute': mins,
                       'studytogether': online_num
                   })


@app.route('/timeIncrease', methods=['POST',])
def time_increase():
    raw_data = request.get_data()
    print(raw_data)
    processed_data = utils.process_data(raw_data)
    id = session.get('user_id')
    mins = processed_data['min']

    database.increase_study_time(id, mins)
    return jsonify(code=200,
                   message="Increase study time successful")


@app.route('/getAllQuestions', methods=['POST',])
def get_question_list():
    raw_data = request.get_data()
    print(raw_data)
    processed_data = utils.process_data(raw_data)
    page = processed_data['page']
    classroom_id = session.get('classroom_id')
    question_list = database.get_question_list(classroom_id, page, num=5)

    if question_list is None:
        return jsonify(code=200, message="list is empty!", questions={})

    # question_list: questions.id, title, image, username, time
    # processed_question_list: id, titleContent, imageUrl, userName, askTime
    processed_question_list = []
    for question in question_list:
        processed_question = {}
        processed_question['id'] = question[0]
        processed_question['titleContent'] = question[1]
        processed_question['imageUrl'] = url_for(
                'static', filename=question[2] if question[2] else "user_pics/default.jpg")
        # if question[2] is None:
        #     processed_question['imageUrl'] = None
        # else:
        #     processed_question['imageUrl'] = url_for(
        #         'static', filename=question[2])
        processed_question['userName'] = question[3]
        processed_question['askTime'] = question[4]
        processed_question_list.append(processed_question)
    
    # debug
    print("app.get_question_list gets: ", raw_data)
    print("app.get_question_list returns: ", processed_question_list)

    return jsonify(code=200,
                       message="Get question successful",
                       questions=processed_question_list)


@app.route('/getQuestionById', methods=['POST',])
def get_question_content():
    # frontend post the question id needed
    raw_data = request.get_data()
    print(raw_data)
    processed_data = utils.process_data(raw_data)
    question_id = processed_data['id']
    question_content = database.get_one_question(question_id)
    if question_content is None:
        return jsonify(code=401, message="error:question should exists!")

    comment_list = database.get_comment_list(question_id)
    # question_content: image, username, content, time
    # comment_list: image, username, content, time, id
    # reply_list: from_user.image, from_user.username, to_user.username, content, time
    # return_data:{avatarUrl, userName, asktime, content, 
    #       comments:[{commenterUrl, userName, commentTime, content, commentId,
    #                  replies:[{fromUserAvatarUrl, fromUserNickName, 
    #                            toUserNickName, replyTime, replyContent}]} ]}
    return_data = {}
    return_data['avatarUrl'] = url_for(
            'static', filename=question_content[0] if question_content[0] else "user_pics/default.jpg")
    # if question_content[0] is None:
    #     return_data['avatarUrl'] = None
    # else:
    #     return_data['avatarUrl'] = url_for(
    #         'static', filename=question_content[0])
    return_data['userName'] = question_content[1]
    return_data['askTime'] = question_content[3]
    return_data['content'] = question_content[2]
    return_data['comments'] = []
    if comment_list is None:
        return jsonify(code=200, message="comment is empty!", question=return_data)

    for comment in comment_list:
        processed_comment = {}
        processed_comment['commenterUrl'] = url_for(
                'static', filename=comment[0] if comment[0] else "user_pics/default.jpg")
        # if comment[0] is None:
        #     processed_comment['commenterUrl'] = None
        # else:
        #     processed_comment['commenterUrl'] = url_for(
        #         'static', filename=comment[0])
        processed_comment['userName'] = comment[1]
        processed_comment['commentTime'] = comment[3]
        processed_comment['content'] = comment[2]
        processed_comment['commentId'] = comment[4]
        processed_comment['replies'] = []
        reply_list = database.get_reply_list(comment[4])
        if reply_list is not None:
            for reply in reply_list:
                processed_reply = {}
                processed_reply['fromUserAvatarUrl'] = url_for(
                        'static', filename=reply[0] if reply[0] else "user_pics/default.jpg")
                # if reply[0] is None:
                #     processed_reply['fromUserAvatarUrl'] = None
                # else:
                #     processed_reply['fromUserAvatarUrl'] = url_for(
                #         'static', filename=reply[0])
                processed_reply['fromUserNickName'] = reply[1]
                processed_reply['toUserNickName'] = reply[2]
                processed_reply['replyTime'] = reply[4]
                processed_reply['replyContent'] = reply[3]
                processed_comment['replies'].append(processed_reply)
        return_data['comments'].append(processed_comment)

    return jsonify(code=200,
                    message="Get question successful",
                    question=return_data)


@app.route('/addQuestion', methods=['POST',])
def insert_question():
    raw_data = request.get_data()
    print(raw_data)
    processed_data = utils.process_data(raw_data)
    classroom_id = session.get('classroom_id')
    user_id = session.get('user_id')
    try:
        database.insert_question(processed_data, user_id, classroom_id)
    # if longer than 255 characters
    except sqlite3.IntegrityError:
        return jsonify(code=409, message="Insert question failed!")
    
    return jsonify(code=200, message="Insert question successful")


@app.route('/addComment', methods=['POST',])
def insert_comment():
    raw_data = request.get_data()
    print(raw_data)
    processed_data = utils.process_data(raw_data)
    question_id = processed_data['questionId']
    user_id = session.get('user_id')
    try:
        comment_id = database.insert_comment(processed_data, user_id, question_id)
    # if longer than 255 characters
    except sqlite3.IntegrityError:
        return jsonify(code=409, message="Insert comment failed!")
    
    # get imageUrl, username using database.fetch_user_info
    user_info = database.fetch_user_info(user_id)
    image_url = url_for('static', \
                        filename=user_info['image'] if user_info['image'] else "user_pics/default.jpg")
    # if user_info['image'] is None:
    #     image_url = None
    # else:
    #     image_url = url_for('static', filename=user_info['image'])
    username = user_info['username']
    comment_info = {
        'commentId': comment_id,
        'imageUrl': image_url,
        'userName': username
    }

    #debug
    print("app.insert_comment returns: ", comment_info)
    
    return jsonify(code=200, message="Insert comment successful", info=comment_info)


@app.route('/sentReply', methods=['POST',])
def insert_reply():
    raw_data = request.get_data()
    print(raw_data)
    processed_data = utils.process_data(raw_data)
    user_id = session.get('user_id')
    comment_id = processed_data['commentId']
    try:
        database.insert_reply(processed_data, user_id, comment_id)
    # if longer than 255 characters
    except sqlite3.IntegrityError:
        return jsonify(code=409, message="Insert reply failed!")
    
    return jsonify(code=200, message="Insert reply successful")


@app.route('/getNewestQuestion', methods=['GET',])
def get_newest_question():
    classroom_id = session.get('classroom_id')
    question_list = database.get_question_list(classroom_id, 0, num=1)

    if question_list is None:
        return jsonify(code=400, message="no question, error!", questions={})

    # question_list: questions.id, title, image, username, time
    # processed_question_list: id, titleContent, imageUrl, userName, askTime
    processed_question_list = []
    for question in question_list:
        processed_question = {}
        processed_question['id'] = question[0]
        processed_question['titleContent'] = question[1]
        processed_question['imageUrl'] = url_for(
            'static', filename=question[2] if question[2] else "user_pics/default.jpg")
        processed_question['userName'] = question[3]
        processed_question['askTime'] = question[4]
        processed_question_list.append(processed_question)

    return jsonify(code=200,
                       message="Get question successful",
                       question=processed_question_list[0])



if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5001')
