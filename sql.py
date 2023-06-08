import sqlite3


db = sqlite3.connect('bot.db', check_same_thread=False)
sql = db.cursor()




def addData(user_id, user_file_name, video, image):     
    sql.execute(f" INSERT INTO users VALUES ('{user_id}','{user_file_name}','{video}','{image}') ")
    db.commit()

def deleteData(us_id):
    sql.execute(f" DELETE FROM users WHERE user_id = '{us_id}'")
    db.commit()
     

def select(fl):
    sql.execute(f" SELECT user_file_name, image, video FROM users WHERE user_id = '{fl}'")
    files = sql.fetchall()
    lis = []
    for k in files:
        lis.append(k)
    return lis
    
    

