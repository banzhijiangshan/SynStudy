import sqlite3
import json
import os

import re


def create_db():
    """
    创建数据库，用于存储记录
    id 存储的是记录的序号
    device 开头的存储的是探针的信息
    剩下的存储的是探针扫描到的设备的记录
    """
    # if "devices_data.db" in os.listdir():
    #     os.remove("devices_data.db")
    conn = sqlite3.connect("user_data.db")
    c = conn.cursor()

    # create a database for virtual classrooms,
    # (id, subject, online people numbers, online people id)
    c.execute('''DROP TABLE IF EXISTS classrooms''')
    c.execute('''CREATE TABLE IF NOT EXISTS classrooms
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    subject VARCHAR(30) NOT NULL UNIQUE,
                    online_num INTEGER DEFAULT 0,
                    CHECK (online_num >= 0),
                    CHECK (online_num <= 100))''')
    c.execute('''DROP TABLE IF EXISTS users''')
    # sex分为0，1和2，分别代表未知，男和女
    # also include a foreign key for classroom id
    # also include a path for user image
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username VARCHAR(30) NOT NULL UNIQUE,
                  password CHAR(60) NOT NULL,
                  email VARCHAR(50) NOT NULL UNIQUE,
                  sex INTEGER DEFAULT 0,
                  age INTEGER DEFAULT NULL,
                  area VARCHAR(30) DEFAULT NULL,
                  hobby VARCHAR(60) DEFAULT NULL,
                  work VARCHAR(30) DEFAULT NULL,
                  design VARCHAR(255) DEFAULT NULL,
                  phone VARCHAR(30) DEFAULT NULL,
                  image VARCHAR(255) DEFAULT NULL,
                  study_time INTEGER DEFAULT 0,
                  classroom_id INTEGER DEFAULT NULL,
                  FOREIGN KEY (classroom_id) REFERENCES classrooms(id))''')

    c.execute('''DROP TABLE IF EXISTS questions''')
    # id, user_id, classroom_id, title, tag, content, time
    c.execute('''CREATE TABLE IF NOT EXISTS questions
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    classroom_id INTEGER NOT NULL,
                    title VARCHAR(255) NOT NULL,
                    tag VARCHAR(255) NOT NULL,
                    content VARCHAR(255) NOT NULL,
                    time VARCHAR(255) NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (classroom_id) REFERENCES classrooms(id))''')
    
    # create comment table (id, user_id, question_id, content, time)
    c.execute('''DROP TABLE IF EXISTS comments''')
    c.execute('''CREATE TABLE IF NOT EXISTS comments
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    question_id INTEGER NOT NULL,
                    content VARCHAR(255) NOT NULL,
                    time VARCHAR(255) NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (question_id) REFERENCES questions(id))''')

    # create reply table (id, user_id, comment_id, content, time, reply_to_id)
    # reply_to_id is the id of reply that this reply replies to
    c.execute('''DROP TABLE IF EXISTS replies''')
    c.execute('''CREATE TABLE IF NOT EXISTS replies
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    comment_id INTEGER NOT NULL,
                    content VARCHAR(255) NOT NULL,
                    time VARCHAR(255) NOT NULL,
                    reply_to_id INTEGER NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (comment_id) REFERENCES comments(id),
                    FOREIGN KEY (reply_to_id) REFERENCES replies(id))''')

    # add math, phy, chem classrooms
    c.execute("INSERT INTO classrooms (subject) VALUES ('math')")
    c.execute("INSERT INTO classrooms (subject) VALUES ('phy')")
    c.execute("INSERT INTO classrooms (subject) VALUES ('chem')")

    conn.commit()
    conn.close()


def insert_register_data(data):
    """
    对于处理过的字节流, 将其分解为数据库中的记录
    """
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()

    username = data["name"]
    password = data["password"]
    email = data["email"]

    c.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
              (username, password, email))

    conn.commit()
    conn.close()


def fetch_pw_and_id(user_input):
    """
    根据学号/用户名/邮箱查找对应的加密后密码和用户id
    """
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()

    # check if user_input is email
    if re.match(r"[^@]+@[^@]+\.[^@]+", user_input):
        query = "SELECT password, id FROM users WHERE email = ?"
        cursor.execute(query, (user_input,))
        result = cursor.fetchone()  # will return a tuple
        conn.close()

        pw = result[0] if result else None
        id = result[1] if result else None

    # check if user_input is username (1-16 characters started with letter)
    elif re.match(r"[a-zA-Z][a-zA-Z0-9]{0,15}", user_input):
        query = "SELECT password, id FROM users WHERE username = ?"
        cursor.execute(query, (user_input,))
        result = cursor.fetchone()
        conn.close()

        pw = result[0] if result else None
        id = result[1] if result else None

    # check if user_input is student id
    elif re.match(r"\d{5}", user_input):
        query = "SELECT password FROM users WHERE id = ?"
        cursor.execute(query, ((int(user_input) - 10000),))
        result = cursor.fetchone()
        conn.close()

        pw = result[0] if result else None
        id = int(user_input) - 10000

    else:
        return (None, None)

    return (pw, id)


def fetch_cur_cnt():
    """
    获取当前数据库中的记录数
    """
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()

    query = "SELECT COUNT(*) FROM users"
    cursor.execute(query)

    result = cursor.fetchone()
    conn.close()

    return result[0] if result else None


def fetch_user_info(id):
    """
    根据id获取用户信息
    """
    conn = sqlite3.connect('user_data.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = "SELECT * FROM users WHERE id = ?"
    cursor.execute(query, (id,))

    result = dict(cursor.fetchone())  # returns a tuple
    conn.close()

    return result if result else None


def update_user_info(id, data):
    """
    根据id和输入的数据修改用户信息
    """
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()

    query = "UPDATE users SET "
    # do when data[key] is not None
    for key in data:
        if data[key] is not None and key != 'id':
            query += key + " = '" + str(data[key]) + "', "

    # only set to given id
    query = query[:-2] + " WHERE id = " + str(id)
    cursor.execute(query)

    conn.commit()
    conn.close()


def get_classroom_id(subject):
    """
    根据课程名获取课程id
    """
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()

    query = "SELECT id FROM classrooms WHERE subject = ?"
    cursor.execute(query, (subject,))

    result = cursor.fetchone()
    conn.close()

    return result[0] if result else None


def enter_classroom(id, classroom_id):
    """
    根据id和class_id修改用户信息和classroom信息
    """
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()

    query = "UPDATE users SET classroom_id = " + \
        str(classroom_id) + " WHERE id = " + str(id)
    cursor.execute(query)

    query = "UPDATE classrooms SET online_num = online_num + 1 WHERE id = " + \
        str(classroom_id)
    cursor.execute(query)

    conn.commit()
    conn.close()


def leave_classroom(id, classroom_id):
    """
    根据id和class_id修改用户信息和classroom信息
    """
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()

    query = "UPDATE users SET classroom_id = NULL WHERE id = " + str(id)
    cursor.execute(query)

    query = "UPDATE classrooms SET online_num = online_num - 1 WHERE id = " + \
        str(classroom_id)
    cursor.execute(query)

    conn.commit()
    conn.close()


def get_study_time(id):
    """
    根据id获取用户学习时间
    """
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()

    query = "SELECT study_time FROM users WHERE id = ?"
    cursor.execute(query, (id,))

    result = cursor.fetchone()
    conn.close()
    mins = result[0]
    hours = mins // 60  # 整除
    mins = mins % 60   # 取余

    return (hours, mins)


def increase_study_time(id, mins):
    """
    根据id和增加的分钟数增加用户学习时间
    """
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()

    query = "UPDATE users SET study_time = study_time + " + \
        str(mins) + " WHERE id = " + str(id)
    cursor.execute(query)

    conn.commit()
    conn.close()


def get_online_num(classroom_id):
    """
    根据classroom_id获取在线人数
    """
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()

    query = "SELECT online_num FROM classrooms WHERE id = ?"
    cursor.execute(query, (classroom_id,))

    result = cursor.fetchone()
    conn.close()

    return result[0] if result else None


def get_question_list(classroom_id, page):
    """
    获取classroom_id对应的最新的10个问题
    """
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()

    # page 0 means get the first 10 questions
    # page 1 means get the second 10 questions
    query = "SELECT questions.id, title, image, username, time \
            FROM questions join users \
            ON users.id = questions.user_id \
            WHERE questions.classroom_id = ? \
            ORDER BY time DESC LIMIT 10 OFFSET ?"

    cursor.execute(query, (classroom_id, page * 10))

    result = cursor.fetchall()
    conn.close()

    # debug
    print("get_question_list result", result)

    return result if result else None


def insert_question(question, user_id, classroom_id):
    """
    将question插入
    """
    #debug
    print("insert question started!")
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()

    #debug
    print("database connected!")

    query = "INSERT INTO questions (user_id, classroom_id, title, tag, content, time) \
             VALUES (?, ?, ?, ?, ?, ?)"
    cursor.execute(query, (user_id, classroom_id, question["title"],
                           question["tag"] if "tag" in question else "Default", 
                           question["content"], question["askTime"]))

    #debug
    print("insert question cursor executed!")

    conn.commit()
    conn.close()

    #debug
    print("insert_question finished!")


def get_one_question(question_id):
    """
    根据question_id获取问题内容
    """
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()

    query = "SELECT image, username, content, time \
            FROM questions join users \
            ON users.id = questions.user_id \
            WHERE questions.id = ?"

    cursor.execute(query, (question_id,))

    result = cursor.fetchone()
    conn.close()

    # debug
    print("get_one_question result", result)

    return result if result else None


def get_comment_list(question_id):
    """
    根据question_id获取评论列表
    """
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()

    query = "SELECT image, username, content, time, id \
            FROM comments join users \
            ON users.id = comments.user_id \
            WHERE question_id = ?"

    cursor.execute(query, (question_id,))

    result = cursor.fetchall()
    conn.close()

    # debug
    print("get_comment_list result", result)

    return result if result else None

def get_reply_list(comment_id):
    """
    根据comment_id获取回复列表
    """
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()

    # from_user_id, from_username, to_user_id, to_username, content, time
    # q:what if replies join users twice?
    # a:use alias
    query = "SELECT from_user.image, from_user.username, to_user.username, content, time \
            FROM replies join users as from_user \
            ON from_user.id = replies.user_id \
            join users as to_user \
            ON to_user.id = replies.reply_to_id \
            WHERE comment_id = ?"

    cursor.execute(query, (comment_id,))

    result = cursor.fetchall()
    conn.close()

    # debug
    print("get_reply_list result", result)

    return result if result else None


def insert_comment(comment, user_id, question_id):
    """
    将comment插入
    """
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()

    query = "INSERT INTO comments (user_id, question_id, content, time) \
             VALUES (?, ?, ?, ?)"
    cursor.execute(query, (user_id, question_id, comment["content"], comment["time"]))

    conn.commit()
    conn.close()


def insert_reply(reply, user_id, comment_id):
    """
    将reply插入
    """
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()

    query = "INSERT INTO replies (user_id, comment_id, content, time, reply_to_id) \
             VALUES (?, ?, ?, ?, ?)"
    cursor.execute(query, (user_id, comment_id, reply["content"], reply["time"], reply["reply_to_id"]))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_db()
