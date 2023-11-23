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
                  time INTEGER DEFAULT 0,
                  classroom_id INTEGER DEFAULT NULL,
                  FOREIGN KEY (classroom_id) REFERENCES classrooms(id))''')

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

    query = "SELECT time FROM users WHERE id = ?"
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

    query = "UPDATE users SET time = time + " + \
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


if __name__ == "__main__":
    create_db()
