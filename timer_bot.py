# #!/usr/bin/python

# # This is a simple bot with schedule timer
# # https://schedule.readthedocs.io
# # -*- coding: utf-8 -*-
# """
# This Example will show you how to use register_next_step handler.

import pygsheets
from email import message
import telebot
from telebot import types
from datetime import datetime
import time

service_file = r'plenary-network-357508-e2922d08b6ea.json'
gc = pygsheets.authorize(service_file=service_file)
sheetname = 'Timelogger'
sh = gc.open(sheetname)
wks = sh.worksheet_by_title('Sheet1')
wksuser = sh.worksheet_by_title('Sheet2')


API_TOKEN = '5577559782:AAGr3X0s8QltH0QlByn-Dqiya5OPvOz8xIQ'

bot = telebot.TeleBot(API_TOKEN)

user_dict = {}

print("Bot getting started..")

class User:
    def __init__(self, name):
        self.timein = name
        self.timeout = None

@bot.message_handler(commands=['help','start'])
def send_help(message):
    msg = bot.reply_to(message,
"""I am TimeLogger bot.\nAvailable commands on this bot\n
Type /timein to login
Type /timeout to logout
Type /status\n\n

""")


@bot.message_handler(commands=['timein'])   
# Timein

def process_timein(message):
    username = message.chat.username
    finduser = wksuser.find(username)
    nofind = int(len(finduser))
    if nofind >= 1:
        try:
            now = datetime.now()
            date_time = now.strftime("%H:%M:%S")
            time = now.strftime("%H:%M:%S")
            date = now.strftime('%m/%d/%y')
            chat_id = message.chat.id
            timein = message.text
            user = User(timein)
            user_dict[chat_id] = user
            user.timein = date_time
            
            if timein == "/timein":
                user_first_name = str(message.chat.first_name)
                user_last_name = str(message.chat.last_name)
                full_name = user_first_name + " "+ user_last_name
                grecord = wks.get_all_records()
                num=2
                for i in range(len(grecord)):
                    num+=1
                    if full_name == grecord[i].get("Name") and date == grecord[i].get("Date"):
                        bot.reply_to(message, f'You already timedin on this day')
                        
                        break
                else: 
                    
                    wks.update_value((num,1),full_name)
                    wks.update_value((num,2),date)
                    wks.update_value((num,3),time)
                    bot.reply_to(message, f'Successfully timein on {str(date_time)}')
                    # timelog = []
                    # timelog.append(str(full_name))
                    # timelog.append(str(date))
                    # timelog.append(str(time))
                    # wks.append_table(timelog)    
                    
                            

        except Exception as e:
            bot.reply_to(message, '')
    else:
        bot.reply_to(message, 'Only Intern member can use this bot')
 
@bot.message_handler(commands=['timeout'])  
# Timeout
def process_timeout(message):
   
    try:
        now2 = datetime.now()
        date_time2 = now2.strftime("%H:%M:%S")
        time2 = now2.strftime("%H:%M:%S")
        timeout = message.text 
        user = User(timeout)
        user.timeout = date_time2
        user_first_name = str(message.chat.first_name)
        user_last_name = str(message.chat.last_name)
        full_name = user_first_name + " "+ user_last_name
        date = now2.strftime('%m/%d/%y')

        if timeout == "/timeout":
            grecord = wks.get_all_records()
            num = 1
            for i in range(len(grecord)):
                num += 1
                if full_name == grecord[i].get("Name") and date == grecord[i].get("Date") and grecord[i].get("Timeout")== '':
                    
                    wks.update_value((num,4),time2)
                    bot.reply_to(message, f'Successfully TIMEOUT on {str(date_time2)}')
                    break
                elif full_name == grecord[i].get("Name") and date == grecord[i].get("Date") and grecord[i].get("Timeout")!= '':

                    bot.reply_to(message, 'You have already TIMED OUT')
            else:
                    bot.reply_to(message, "You haven't TIMED IN yet today")   


    except Exception as e:
        bot.reply_to(message, '')

@bot.message_handler(commands=['status'])  
def process_status(message):
    user_first_name = str(message.chat.first_name) 
    user_last_name = str(message.chat.last_name)
    full_name = user_first_name + " "+ user_last_name
    now = datetime.now()
    date = now.strftime('%m/%d/%y')
    grecord = wks.get_all_records()
    num = 1
    for i in range(len(grecord)):
        num += 1
        if full_name == grecord[i].get("Name") and date == grecord[i].get("Date") and grecord[i].get("Timein")!= '' and grecord[i].get("Timeout")!= '':
            bot.reply_to(message, f'Date {date}\nTimein: {grecord[i].get("Timein")}\nTimeout: {grecord[i].get("Timeout")}')
            break
        elif full_name == grecord[i].get("Name") and date == grecord[i].get("Date") and grecord[i].get("Timein")!= '' and grecord[i].get("Timeout")== '':
            bot.reply_to(message, f'Date {date}\nTimein: {grecord[i].get("Timein")}\nTimeout: NONE')
            break
    else:
        bot.reply_to(message, "You haven't TIMED IN yet today")





# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

bot.infinity_polling()


# import time, threading, schedule
# import pygsheets
# from telebot import TeleBot
# from datetime import datetime


# service_file = r'C:\Users\Will\OneDrive\Desktop\timelogger\plenary-network-357508-e2922d08b6ea.json'
# gc = pygsheets.authorize(service_file=service_file)
# sheetname = 'Timelog'
# sh = gc.open(sheetname)
# wks = sh.worksheet_by_title('Sheet1')


# API_TOKEN = '5516314811:AAFEuI7njv4zUDHJ-rSkaLmmuslDq0BIymQ'
# bot = TeleBot(API_TOKEN)


# @bot.message_handler(commands=['help', 'start'])
# def send_welcome(message):
#     bot.reply_to(message, "Nexlogic TimeLogger Intern 2022")


# @bot.message_handler(commands=['timein'])
# def timein(message):
#     now = datetime.now()
#     time = now.strftime('%H:%M%p')
#     date = now.strftime('%m/%d/%y')
#     date_time = now.strftime("Successfully Timein on %m/%d/%y - %H:%M:%S%p")
#     bot.reply_to(message, date_time)
#     wks.update_value('B2', date)
#     wks.update_value('C2', time)


# @bot.message_handler(commands=['timeout'])
# def timeout(message):
#     now = datetime.now()
#     time = now.strftime('%H:%M%p')
#     date_time = now.strftime("Successfully Timeout on %m/%d/%y - %H:%M:%S%p")
#     bot.reply_to(message, date_time)
#     wks.update_value('D2', time)


# if __name__ == '__main__':
#     threading.Thread(target=bot.infinity_polling, name='bot_infinity_polling', daemon=True).start()
#     while True:
#         schedule.run_pending()
#         time.sleep(1)

