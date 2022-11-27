import telebot
import requests
import time
import io
from telebot import types
from random import randint

bot = telebot.TeleBot("5952703055:AAG91Q_WUcQ60J_qKg2JMPB8HWFmcCcIxSA", parse_mode=None)

number = None
step = 1
is_started = False
evl = None
result = 0

markup = types.ReplyKeyboardMarkup()
itembtn1 = types.KeyboardButton('котик')
itembtn2 = types.KeyboardButton('погода')
itembtn3 = types.KeyboardButton('привет')
itembtn4 = types.KeyboardButton('регистрация')
itembtn5 = types.KeyboardButton('играть')
itembtn6 = types.KeyboardButton('вычислить')
markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6)



@bot.message_handler(commands=["start", "help", "hello", "notify"])
def send_welcome(message):
    bot.reply_to(message, "привет, " + message.from_user.first_name, reply_markup=markup)
    data = open("user.txt", "r", encoding = "utf-8")
    users = data.readlines()
    for id in users:
        try:
            bot.send_message(id[:-1], "оповещение")
        except telebot.apihelper.ApiTelegramException:
            print(f"Соббщение пользователю {id[:-1]} отправить не удалось")
    data.close()



@bot.message_handler(content_types = ["text"])
def hello_user(message):
    global is_started
    global number
    global step
    global evl
    global result
    
    if evl:
        input_evl = message.text
        result = eval(input_evl)
        bot.send_message(message.from_user.id, f"Результат равен {result}")
        evl = False 

    if is_started:
        if message.text.isdigit():
            input_number = int(message.text)
            if input_number > number:
                bot.send_message(message.from_user.id, "Меньше, гадай дальше!")
            elif input_number < number:
                bot.send_message(message.from_user.id, "Больше, гадай дальше!")
            elif input_number == number:
                is_started = False
                bot.send_message(message.from_user.id, f"Ты победил! Я загадал число {number}. Тебе потребовалось {step} хода(-ов).")
            else:
                bot.send_message(message.from_user.id, "Ты кожанный...")
                step += 1 
        else:
            bot.send_message(message.from_user.id, "Введи только число")
    else: 
        print(f"{message.from_user.id} {message.from_user.first_name} {message.from_user.last_name}: {message.text}")
        if "привет" in message.text:
            bot.reply_to(message, "привет, " + message.from_user.first_name)
        elif message.text == "играть":
            number = randint(1, 1001)
            is_started = True
            step = 1
            bot.reply_to(message, f"Я загадал число от 1 до 1000. Давай угадывай!!!. Введи первое число. {number}")
        elif message.text == "погода":
            r = requests.get('https://wttr.in/?0T')
            print(r.text)
            bot.reply_to(message, r)
        elif message.text == "котик":
            r = f"https://cataas.com/cat?t=${time.time()}"
            bot.send_photo(message.chat.id, r)    
        elif message.text == "файл":
            data = open("user_message.txt", encoding = "utf-8")
            bot.send_document(message.chat.id, data)
            data.close()
        elif message.text == "вычислить":
            evl = True
            bot.send_message(message.from_user.id, "Пришли выражение")
        elif message.text == "регистрация":
            user_id = str(message.from_user.id) + "\n"
            data = open ("user.txt", "r+", encoding = "utf-8")
            try:            
                lines = data.readlines()
                if user_id not in lines:
                    data.writelines(str(message.from_user.id) + "\n")
                    bot.send_message(message.from_user.id, "Регистрация прошла")
                else:
                    bot.send_message(message.from_user.id, "Данный id уже есть")
            except io.UnsupportedOperation:
                data.writelines(str(message.from_user.id) + "\n")
                bot.send_message(message.from_user.id, "Регистрация прошла")
            data.close()
    
# @bot.message_handler(commands=['notify'])
# def notify(message):
#     print(1)
#     data = open("user.txt", "r", encoding = "utf-8")
#     users = data.read().removesuffix("\n")
#     print(users) 

bot.infinity_polling()










    