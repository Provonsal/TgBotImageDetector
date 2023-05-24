import telebot
import multiprocessing
#from detect import run as NN
import os
import time
from pathlib import Path
import shutil

bot = telebot.TeleBot('6086665182:AAHhUQiu6Crx_RaDUkSML3Ws9sZDCzaeDsg')
a = 1
b = 0
c = 0

def load_img(message):
    def download_images(message):
        file_info = bot.get_file(message.photo[-1].file_id)
        
        downloaded_file = bot.download_file(file_info.file_path)
        user_id = str(message.from_user.id) + '/' 
        if not os.path.isdir('bot-images/' + user_id):
            os.mkdir('bot-images/' + user_id) 
        file_name = file_info.file_path.replace('photos/', '')
        
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
    file_name = message.video.file_id + '.mp4'
    print(message, type(user_id), type(file_name))
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
                if len(photos) < 10:
                    
                    break
                elif len(medias) == 10:
                    print('sosat')
                    bot.send_media_group(chat, medias)
                        
                    medias = []
                    if len(photos_copy) < 10:
                        
                        break
                medias.append(telebot.types.InputMediaPhoto(open(f'{path}{i}', 'rb')))
                print('len of photos: ',len(photos_copy))
                photos_copy.remove(i)
                    
            
            for i in photos_copy:
                print('second')
                print('len of photos: ', len(photos_copy))
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
        bot.send_message(chat, 'All processed files have sent. Now you can press "Load files again" and try again')
        
    sending_back(chat)

def process_creater(file, func, message, kwargs={}):
    
    if file == 1:
        proc1 = multiprocessing.Process(target = func, args=(message,))
        proc1.start()
    if file == 0:
        proc2 = multiprocessing.Process(target = func, args=(message,))
        proc2.start()
    else:
        proc2 = multiprocessing.Process(target = func, args=(message,))
        proc2.start()

@bot.message_handler(commands=['start']) # 111111111111111111111111111111111111
def main1(message):
    def main2(message):
    
        global a
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width = 1)
        button_1 = telebot.types.KeyboardButton('Load files')
        
        text = """Hello, stranger. 

If you want me to recognize images on your screenshot\video, then press the button "Load files" and follow the instructions.
        
After you send me your files, wait a while to let my pc download files

Please do not break the sequence of actions.
    """
        markup.add(button_1)
        bot.send_message(message.chat.id, text, reply_markup = markup)
        a = 1
    main2(message)
        
    
@bot.message_handler(func=lambda message: message.text == "Load files" or message.text == "Load files again") # 22222222222222222222222222222222222
def bum(message):
    def bum2(message):
        global a, b
        chat = message.chat.id
        user_id = str(message.from_user.id)
        
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width = 1)
        button_1 = telebot.types.KeyboardButton('End loading')
        
        text = """Okay, send me your files to load. I'll load them"""
        
        markup.add(button_1)
        
        bot.send_message(message.chat.id, text, reply_markup = markup)
    
        
        def deleting():
            path = f'C:/Users/Provonsal/source/repos/yolov5/bot-images/{user_id}'
            try:
                shutil.rmtree(path)
            except:
                return
            time.sleep(5)
            bot.send_message(chat, 'Deleting complete. Now you can send me files')
            
        bot.send_message(chat, 'Deleting previous files from my storage...')
        
        deleting()
        a = 2
        b = 1
    
    bum2(message)
    
@bot.message_handler(func=lambda message: message.text == "End loading") # 3333333333333333333333333333333333333333
def end_loading(message):
    def end_loading1(message):
        global a, b
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width = 1)
        button_1 = telebot.types.KeyboardButton('Process the files')
        
        text = """Okay, loading is done, now press the button "Process the files" and magic begin """
        
        markup.add(button_1)
        
        bot.send_message(message.chat.id, text, reply_markup = markup)
        a = 3
        b = 0
    
    end_loading1(message)

@bot.message_handler(content_types=['photo', 'video'])   # 44444444444444444444444444444444444444444 
def checker(message):
    global b
    def loader(message):        
        content = message.content_type
        if content == 'photo':
            time.sleep(1)
            process_creater(1, load_img, message)
        elif content == 'video':
            time.sleep(1)
            process_creater(0, load_vid, message)
    
        
        
    if b:
        loader(message)

@bot.message_handler(func=lambda message: message.text == "Process the files") # 55555555555555555555555555555555
def rep1(message):
    def rep2(message):
        global a
        text = """Well let's start.
It will take some time, please wait.
Results will be automaticaly send here.
DO NOT press the button "Load files again" until it end otherwise it wont process the files.
    """
        
        process_creater(0, NeurN, message)
        
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width = 1)
        button_1 = telebot.types.KeyboardButton('Load files again')
        
        
        markup.add(button_1)
        
        bot.send_message(message.chat.id, text, reply_markup = markup)
        a = 1
    rep2(message)

  
    

    
if __name__ == '__main__':
    
    
    bot.polling()