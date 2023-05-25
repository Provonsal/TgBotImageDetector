import sqlite3
import random


db = sqlite3.connect('bot.db')
sql = db.cursor()

#sql.execute(""" CREATE TABLE IF NOT EXISTS users (user_id TEXT, user_file_name TEXT) """)
#db.commit()


def addData(user_id, user_file_name):     
    db.execute(f" INSERT INTO users VALUES ('{user_id}','{user_file_name}') ")
    db.commit()

def deleteData(fl):
    db.execute(f" DELETE FROM users WHERE user_file_name = '{fl}'")
    db.commit()

def select(fl):
    db.execute(f" SELECT user_file_name FROM users WHERE user_file_name = '{fl}'")