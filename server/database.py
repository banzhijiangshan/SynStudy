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
    c.execute('''DROP TABLE IF EXISTS users''')
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username VARCHAR(255) NOT NULL UNIQUE,
                  password CHAR(60) NOT NULL,
                  email VARCHAR(255) NOT NULL UNIQUE)''')
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

    c.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, password, email))

    conn.commit()
    conn.close()

def fetch_pw(user_input):
    """
    根据学号/用户名/邮箱查找对应的加密后密码
    """
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()

    # check if user_input is email
    if re.match(r"[^@]+@[^@]+\.[^@]+", user_input):
        query = "SELECT password FROM users WHERE email = ?"
        cursor.execute(query, (user_input,))
    # check if user_input is username (4-16 characters started with letter)
    elif re.match(r"[a-zA-Z][a-zA-Z0-9]{3,15}", user_input):
        query = "SELECT password FROM users WHERE username = ?"
        cursor.execute(query, (user_input,))
    # check if user_input is student id
    elif re.match(r"\d{5}", user_input):
        query = "SELECT password FROM users WHERE id = ?"
        cursor.execute(query, ((int(user_input) - 10000),))
    else:
        return None

    result = cursor.fetchone()
    conn.close()

    return result[0] if result else None

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

if __name__ == "__main__":
    create_db()

