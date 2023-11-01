import sqlite3
import json
import os


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
                  password CHAR(60) NOT NULL)''')
    conn.commit()
    conn.close()


def insert_data(data):
    """
    对于处理过的字节流, 将其分解为数据库中的记录
    """
    conn = sqlite3.connect('devices_data.db')
    c = conn.cursor()

    username = data["username"]
    password = data["password"]

    c.execute(
    "INSERT INTO devices (username, password) VALUES (?, ?)",
    (username, password)

    conn.commit()
    conn.close()

def fetch_data(username):
    """
    根据用户名查找对应的加密后密码
    """
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()

    query = "SELECT password FROM users WHERE username = ?"
    cursor.execute(query, (username,))
    result = cursor.fetchone()

    conn.close()

    return result[0] if result else None

if __name__ == "__main__":
    create_db()

