import sqlite3

# подключение к БД
db = sqlite3.connect('bot.db', check_same_thread=False)

# создание курсора для взаимодействия с БД
sql = db.cursor()

# функция добавления данных в БД
def addData(user_id, user_file_name, video, image):     
    sql.execute(f" INSERT INTO users VALUES ('{user_id}','{user_file_name}','{video}','{image}') ")
    db.commit()

# функция удаления данных конкретного пользователя
def deleteData(us_id):
    sql.execute(f" DELETE FROM users WHERE user_id = '{us_id}'")
    db.commit()

# функция по выбору данных конкретного пользователя и добавления их в список      
def select(fl):
    sql.execute(f" SELECT user_file_name, image, video FROM users WHERE user_id = '{fl}'")
    files = sql.fetchall()
    lis = []
    for k in files:
        lis.append(k)
    return lis
    
    

