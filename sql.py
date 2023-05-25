import sqlite3
import random


db = sqlite3.connect('bot.db', check_same_thread=False)
sql = db.cursor()

#sql.execute(""" CREATE TABLE IF NOT EXISTS users (user_id TEXT, user_file_name TEXT) """)
#db.commit()


def addData(user_id, user_file_name):     
    sql.execute(f" INSERT INTO users VALUES ('{user_id}','{user_file_name}') ")
    db.commit()

def deleteData(fl):
    sql.execute(f" DELETE FROM users WHERE user_id = '{fl}'")
    db.commit()
     

def select(fl):
    sql.execute(f" SELECT user_file_name FROM users WHERE user_id = '{fl}'")
    files = sql.fetchall()
    lis = []
    for k in files:
        lis.append(k[0])
    return lis
    
    

select('999999')