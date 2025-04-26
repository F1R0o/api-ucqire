import sqlite3
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

def connect_db_api():
    db_path = os.path.join(BASE_DIR, "../data/database.db")
    return sqlite3.connect(db_path)

def connect_db_api2():
    db_path = os.path.join(BASE_DIR, "../data/data2.db")
    return sqlite3.connect(db_path)


