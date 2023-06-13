# coding=utf-8

import telebot
import multiprocessing
import os
import time
from pathlib import Path
import shutil
import sql

# задается токен бота
bot = telebot.TeleBot('токен бота')

# bool для шлюза загрузки, по умолчанию False
b = 0 

# функция добавления названия файлов изображений в БД
def load_img(message):
    
    user_id = str(message.from_user.id)
    file_info = bot.get_file(message.photo[-1].file_id)
    file_path = file_info.file_path
    
    sql.addData(user_id, file_path, 0, 1)

# функция скачивания изображений для конкретного пользователя по списку взятого из БД    
def download_images(message, user_id):
        
        # достаем список файлов принадлежат конкретному пользователю
        lis = sql.select(user_id)
        print(lis)
        lis_i = []
        user_id = str(user_id) + '/' 

        # итерация первого списка созданного из записей БД и добавление их во второй список если image = 1
        for i in lis:
            
            if i[1]:
                lis_i.append(i[0])
        
        # итерация второго списка и загрузка каждого элемента с серверов телеграм
        for i in lis_i:
            
            downloaded_file = bot.download_file(i)
            print(user_id)

            if not os.path.isdir('bot-images/' + user_id):
                os.mkdir('bot-images/' + user_id) 
            file_name = i.replace('photos/', '')
        
            src = 'bot-images/'+ user_id + file_name
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)

        text = f'{len(lis_i)} images have loaded'
        bot.send_message(message.chat.id, text)

# функция добавления названия файлов видеофайлов в БД
def load_vid(message):
    
    user_id = str(message.from_user.id)
    file_info = bot.get_file(message.video.file_id)
    file_path = file_info.file_path
    
    sql.addData(user_id, file_path, 1, 0)

# функция скачивания видеофайлов для конкретного пользователя по списку взятого из БД
def download_videos(message, user_id):
    
    # достаем список файлов принадлежат конкретному пользователю
    lis = sql.select(user_id)
    print(lis)
    lis_v = []

    # итерация первого списка созданного из записей БД и добавление их во второй список если video = 1
    for i in lis:

        if i[2]:
            
            lis_v.append(i[0])
    
    # итерация второго списка и загрузка каждого элемента с серверов телеграм
    for i in lis_v:
        
        downloaded_file = bot.download_file(i)
        user_id = user_id + '/'
        if not os.path.isdir('bot-images/' + user_id):
            os.mkdir('bot-images/' + user_id) 
        file_name = i.replace('videos/', '') 
    
        src = 'bot-images/'+ user_id + file_name
        
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        
    text = f'{len(lis_v)} videos have loaded'
    bot.send_message(message.chat.id, text)
        
    
# функция обработки файлов нейронной сетью и дальнейшее отправление переработанных данных обратно пользователю
def NeurN(message, user_id): 
    
    from detect import run as NN 

    # id чата с пользователем
    chat = message.chat.id
    
    # путь для каждого пользователя
    path = f'C:/Users/Provonsal/source/repos/yolov5/bot-images/{user_id}/' 
    
    # функция запуска нейросеть на детекцию и передачи ей аргументов
    NN(**{'source':path, 'project':path}) 

    # функция отправки файлов обратно пользователю
    def sending_back(chat):

        # путь откуда брать обработанные файлы
        path = f'C:/Users/Provonsal/source/repos/yolov5/bot-images/{user_id}/exp/'
        
        # list of directory
        arti = os.listdir(path) 

        # вспомогательные листы
        medias = [] 
        photos = [] 
        videos = [] 
        
        # функция отправки обработанных фото обратно пользователю
        def otpravka_photo(medias, photos, chat):
            
            photos = photos
            photos_copy = photos.copy()
            
            for i in photos:

                print('first')
                print('len of medias: ',len(medias))
                print('len of photos: ',len(photos))

                # если количество фото меньше 10, то цикл прерывает и начинается другой где фото отправляються по отдельности
                if len(photos) < 10:
                    break

                # если количество фото равно десяти, то все фото добавляются в список и 
                # отправляются единой пачкой 10 шт
                elif len(photos) == 10:
                    
                    for i in photos:
                        medias.append(telebot.types.InputMediaPhoto(open(f'{path}{i}', 'rb')))
                    
                    bot.send_media_group(chat, medias)   
                    medias = []

                    break

                # если длина вспомогательного списка равна 10, то происходит отправка пачки фотографий
                elif len(medias) == 10:
                    
                    
                    bot.send_media_group(chat, medias)  
                    medias = []

                    # если кол-во оставшихся фото меньше 10 то цикл полность прерывается и начинается другой
                    # в котором происходит отправка фото по одной штуки
                    if len(photos_copy) < 10:
                        
                        break
                
                # если ни одно условие не сработало, то фото добавляется в вспомогательный список и итерируется дальше
                # пока не сработает одно из условий
                medias.append(telebot.types.InputMediaPhoto(open(f'{path}{i}', 'rb')))
                print('len of photos_copy: ',len(photos_copy))
                
                # удаление отправленных фото из копии списка
                photos_copy.remove(i)
            
            # если общее количество фото не равно 10, то начинается отправка по одному
            if len(photos) != 10:

                for i in photos_copy:

                    print('second')
                    print('len of photos_copy: ', len(photos_copy))

                    with open(f'{path}{i}', 'rb') as photo:
                        bot.send_photo(chat,photo)
                        medias = []
            
        # функция отправки обработанных видео обратно пользователю
        def otpravka_vid(videos, chat):

            # цикл отправки видео по одному
            for i in videos:

                print('second')
                print('len of videos: ', len(videos))

                with open(f'{path}{i}', 'rb') as video:
                    print(i)
                    bot.send_video(chat,video)
        # сортировка файлов по их типу: фото или видео; исходя из суффикса    
        for i in arti:

            format = Path(f'{path}{i}').suffix

            if format == '.png' or format == '.jpg' or format == '.jpeg':

                print('raz')
                photos.append(i)

            elif format == '.mp4':

                print('dva')
                print(i)
                videos.append(i)
        
        # вызов функций по отправке фото и видео
        otpravka_photo(medias, photos, chat)
        otpravka_vid(videos, chat)
        
        markup = telebot.types.InlineKeyboardMarkup(row_width = 1)
        button_1 = telebot.types.InlineKeyboardButton(text='Load files again', callback_data='Load files')
        markup.add(button_1)

        bot.send_message(chat, 'All processed files have sent. Now you can press "Load files again" and try again', reply_markup = markup)
        
    sending_back(chat)

# функция для создания множества независимых друг от друга процессов
def process_creater(file, func, args):
    
    if file == True:

        print('создаю процесс 1')
        proc1 = multiprocessing.Process(target = func, args=args)
        proc1.start()

    elif file == False:

        print('создаю процесс 2')
        proc2 = multiprocessing.Process(target = func, args=args)
        proc2.start()
    

# функция загрузчика, который создает необходимые процессы для каждого файла для ускорения быстро действия
def loader(message):
    
    content = message.content_type

    if content == 'photo':

        time.sleep(1)
        print('Создаю процесс добавления фото в бд') 
        process_creater(1, load_img, (message,))

    elif content == 'video':

        print('Создаю процесс добавления видео в бд')
        time.sleep(1)
        process_creater(0, load_vid, (message,))

# декоратор для обработки входящих изображений, этот отслеживает команду старт
# и запускает функцию main если была обнаружена команда старт
@bot.message_handler(commands=['start']) 
def main1(message):
    
    global a

    markup = telebot.types.InlineKeyboardMarkup(row_width = 1)
    button_1 = telebot.types.InlineKeyboardButton(text='Next step: file loading', callback_data='Load files')
        
    text = """Hello, stranger. 

I'm a bot, my name is 1pd8 and I can recognize images on your screenshot(s) or video(s).
        
Please press the button below ⬇ to continue. 
"""
    markup.add(button_1)

    bot.send_message(message.chat.id, text, reply_markup = markup)

# функция для сообщения пользователю о начале обработки и запуск функции с нейросетью
def processing(message, real_user_id):
    
    global a
    
    text = """Well let's start.
This process will take a while, please wait.
Results will be automaticaly send here.
"""
       
    markup = telebot.types.InlineKeyboardMarkup(row_width = 1)
    button_1 = telebot.types.InlineKeyboardButton(text='Load files again', callback_data='Load files')
        
    markup.add(button_1)
        
    bot.send_message(message.chat.id, text)  
    NeurN(message, real_user_id)

# функция конца загрузки, запускает процессы для загрузки изображений
#  из списка и закрывает шлюз добавления файлов в БД
def end_loading(message, real_user_id):
    
    global b
        
    markup1 = telebot.types.ReplyKeyboardRemove()
    markup2 = telebot.types.InlineKeyboardMarkup(row_width = 1)
    button_1 = telebot.types.InlineKeyboardButton(text='Load files again', callback_data='Load files')
        
    text1 = """Understood. Downloading files. """
    text2 = """ Files are downloaded. Starting processing... """
    
    path = f'C:/Users/Provonsal/source/repos/yolov5/bot-images/{real_user_id}'

    markup2.add(button_1)
    
    bot.send_message(message.chat.id, text1, reply_markup = markup1)

    print('Создаю процесс загрузки фотографии 1111')
    proc1 = multiprocessing.Process(target = download_images, args=(message,real_user_id))
    proc1.start()

    print('Создаю процесс загрузки видео 1111')
    proc2 = multiprocessing.Process(target = download_videos, args=(message,real_user_id))
    proc2.start()
    
    proc1.join()
    proc2.join()

    b = 0 # закрытие шлюза загрузки файлов

    bot.send_message(message.chat.id, text2)

    if os.path.exists(path):
        process_creater(0, processing, (message,real_user_id))
    else:
        bot.send_message(message.chat.id, 'Sorry, but there is no files to process.', reply_markup=markup2)
        
# декоратор отслеживающий коллбеки от инлайн кнопок
# и запускающий функцию bum_main в случае обнаружения коллбека
@bot.callback_query_handler(func=lambda call: True) 
def bum_main(call):
    
    real_user_id = str(call.from_user.id)
    # функция начала записи имен файлов в БД для каждого конкретного пользователя
    def start_loading(message, real_user_id):
        
        global b

        chat = message.chat.id

        path = f'C:/Users/Provonsal/source/repos/yolov5/bot-images/{real_user_id}'

        # функция очистки директори каждого юзера при попытке повторной загрузки 
        # чтобы исключить захламление диска
        def deleting(real_user_id):

            sql.deleteData(real_user_id)
            
            bot.send_message(chat, 'Deleting previous files from my storage...')
            
            print(real_user_id, 'deleting')
            shutil.rmtree(path)
            
            time.sleep(5)
            bot.send_message(chat, 'Deleting complete.')
            
        if os.path.exists(path):
            deleting(real_user_id)

        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True)
        button_1 = telebot.types.KeyboardButton(text="✅ i'm done, please load these files ✅")
        
        text = """Okay let's start, send me your files. It can be photos or videos."""
        
        markup.add(button_1)
        
        bot.send_message(message.chat.id, text, reply_markup = markup)

        b = 1 # открытие шлюза для загрузки файлов
    
    dict_1 = {'Load files':start_loading}
    
    if call.data in dict_1:
        dict_1[call.data](call.message, real_user_id)            

# декоратор, который отслеживает то когда пользователь говорит что отправил все файлы, которые хотел
@bot.message_handler(func= lambda message: message.text == "✅ i'm done, please load these files ✅")
def jopa(message):
    
    user_id = str(message.from_user.id)
    process_creater(1, end_loading, (message, user_id) ) 

# декоратор отслеживающий фото и видео
@bot.message_handler(content_types=['photo', 'video'])    
def checker(message):
    
    global b
    
    if b:

        print('шлюз открыт')
        loader(message)  
    
if __name__ == '__main__':
    
    bot.polling()