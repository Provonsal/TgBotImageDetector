# coding=utf-8

import telebot
import multiprocessing
#from detect import run as NN
import os
import time
from pathlib import Path
import shutil
import threading
import sql

bot = telebot.TeleBot('6086665182:AAHhUQiu6Crx_RaDUkSML3Ws9sZDCzaeDsg')

b = 0


def load_img(message, s):
    s = s
    user_id = str(message.from_user.id)
    file_info = bot.get_file(message.photo[-1].file_id)
    file_path = file_info.file_path
    
    sql.addData(user_id, file_path)
    
    def download_images(message):
        user_id = str(message.from_user.id)
        lis = sql.select(user_id)
        print(lis)
        for i in lis:
            downloaded_file = bot.download_file(i)
        
            user_id = str(message.from_user.id) + '/' 
            if not os.path.isdir('bot-images/' + user_id):
                os.mkdir('bot-images/' + user_id) 
            file_name = i.replace('photos/', '')
        
            src = 'bot-images/'+ user_id + file_name
        
            print(src)
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
        
            text = f'{file_name} have loaded'
        
        
        bot.send_message(message.chat.id, text)
       
    download_images(message)        
    

def load_vid(message):
    
    file_info = bot.get_file(message.video.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    user_id = str(message.from_user.id) + '/'
    if not os.path.isdir('bot-images/' + user_id):
        os.mkdir('bot-images/' + user_id) 
    file_name = message.video.file_id + '.mp4' if message.video.file_name == None else message.video.file_name
    
    src = 'bot-images/'+ user_id + file_name
        
        
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)
        
    text = f'{file_name} have loaded'
    bot.send_message(message.chat.id, text)
        
    
        
def NeurN(message): 
    from detect import run as NN
    chat = message.chat.id
    user_id = str(message.from_user.id)
    path = f'C:/Users/Provonsal/source/repos/yolov5/bot-images/{user_id}/'
    NN(**{'source':path, 'project':path})
    def sending_back(chat):
        path = f'C:/Users/Provonsal/source/repos/yolov5/bot-images/{user_id}/exp/'
        arti = os.listdir(path) # list of directory
        medias = [] # help list
        photos = [] # list for photo
        videos = [] # list for videos
        def suka(medias, photos, chat):
            
            photos = photos
            photos_copy = photos.copy()
            
            for i in photos:
                print('first')
                print('len of medias: ',len(medias))
                print('len of photos: ',len(photos))
                if len(photos) < 10:
                    
                    break
                elif len(photos) == 10:
                    print('sosat')
                    for i in photos:
                        medias.append(telebot.types.InputMediaPhoto(open(f'{path}{i}', 'rb')))
                    bot.send_media_group(chat, medias)   
                    medias = []
                    break
                elif len(medias) == 10:
                    print('sosat')
                    
                    bot.send_media_group(chat, medias)  
                    medias = []
                    if len(photos_copy) < 10:
                        
                        break
                medias.append(telebot.types.InputMediaPhoto(open(f'{path}{i}', 'rb')))
                print('len of photos_copy: ',len(photos_copy))
                photos_copy.remove(i)
                    
            if len(photos) != 10:
                for i in photos_copy:
                    print('second')
                    print('len of photos_copy: ', len(photos_copy))
                    with open(f'{path}{i}', 'rb') as photo:
                        bot.send_photo(chat,photo)
                        medias = []
            
        
        def blyat(videos, chat):
            for i in videos:
                print('second')
                print('len of videos: ', len(videos))
                with open(f'{path}{i}', 'rb') as video:
                    print(i)
                    bot.send_video(chat,video)
            
        for i in arti:
            format = Path(f'{path}{i}').suffix
            if format == '.png' or format == '.jpg' or format == '.jpeg':
                print('raz')
                photos.append(i)
            elif format == '.mp4':
                print('dva')
                print(i)
                videos.append(i)
        suka(medias, photos, chat)
        blyat(videos, chat)
        markup = telebot.types.InlineKeyboardMarkup(row_width = 1)
        button_1 = telebot.types.InlineKeyboardButton(text='Load files again', callback_data='Load files')
        
        
        markup.add(button_1)
        bot.send_message(chat, 'All processed files have sent. Now you can press "Load files again" and try again', reply_markup = markup)
        
    sending_back(chat)

def process_creater(file, func, message, kwargs={}):
    
    

    if file == True:
        print('создаю процесс 1')
        s = 0
        proc1 = multiprocessing.Process(target = func, args=(message, s,))
        
        proc1.start()   
    elif file == False:
        print('создаю процесс 2')
        proc2 = multiprocessing.Process(target = func, args=(message,))
        proc2.start()
    

@bot.message_handler(commands=['start']) # 111111111111111111111111111111111111
def main1(message):
    global a
    markup = telebot.types.InlineKeyboardMarkup(row_width = 1)
    button_1 = telebot.types.InlineKeyboardButton(text='Load files', callback_data='Load files')
        
    text = """Hello, stranger. 

If you want me to recognize images on your screenshot\video, then press the button "Load files" and follow the instructions.
        
After you send me your files, wait a while to let my pc download files

Please do not break the sequence of actions.
"""
    markup.add(button_1)
    bot.send_message(message.chat.id, text, reply_markup = markup)
    
    
        
    
@bot.callback_query_handler(func=lambda call: True) # 22222222222222222222222222222222222
def bum_main(call):
    
    

    
    
    
    def start_loading(message):
        
        global b
        chat = message.chat.id
        user_id = str(message.from_user.id)
        print(user_id)
        path = f'C:/Users/Provonsal/source/repos/yolov5/bot-images/{user_id}'
        def deleting():
            sql.deleteData(user_id)
            bot.send_message(chat, 'Deleting previous files from my storage...')
            print(user_id)
            
            try:
                print('deleting')
                shutil.rmtree(path)
            except:
                return
            time.sleep(5)
            bot.send_message(chat, 'Deleting complete.')
            
        
        #if os.path.exists(path):
        deleting()

        markup = telebot.types.InlineKeyboardMarkup(row_width = 1)
        button_1 = telebot.types.InlineKeyboardButton(text='End loading', callback_data='End loading')
        
        text = """Okay, send me your files to load. I'll load them"""
        
        markup.add(button_1)
        
        bot.send_message(message.chat.id, text, reply_markup = markup)
        b = 1
    
    
    def end_loading(message):
        global b
        markup = telebot.types.InlineKeyboardMarkup(row_width = 1)
        button_1 = telebot.types.InlineKeyboardButton(text='Process the files', callback_data='Process the files')
        
        text = """Okay, loading is done, now press the button "Process the files" and magic begin """
        
        markup.add(button_1)
        
        bot.send_message(message.chat.id, text, reply_markup = markup)
        
        b = 0
    
       
    
    def processing(message):
        global a
        text = """Well let's start.
It will take a while, please wait.
Results will be automaticaly send here.
"""
        
        process_creater(0, NeurN, message)
        
        markup = telebot.types.InlineKeyboardMarkup(row_width = 1)
        button_1 = telebot.types.InlineKeyboardButton(text='Load files again', callback_data='Load files')
        
        
        markup.add(button_1)
        
        bot.send_message(message.chat.id, text)
    
    dict_1 = {'Load files':start_loading,
              'End loading':end_loading,
              'Process the files':processing,
              }         
    if call.data in dict_1:
        dict_1[call.data](call.message)            

f = {}
@bot.message_handler(content_types=['photo', 'video'])   # 44444444444444444444444444444444444444444 
def checker(message):
    global b, f
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    def loader(message):        
        content = message.content_type
        if content == 'photo':
            time.sleep(1)
            print('Создаю процесс загрузки фотографии')
            process_creater(1, load_img, message)
        elif content == 'video':
            print('Создаю процесс загрузки видео')
            time.sleep(1)
            process_creater(0, load_vid, message)
    
        
        
    if b:
        print('1')
        loader(message)  
    

    
if __name__ == '__main__':
    manager = multiprocessing.Manager()
    d = manager.dict()

    bot.polling()