import time
from datetime import timedelta

__author__ = 'edx'
from utils.helper_functions import *
import telebot
import telegram
import paramiko

TOKEN = '161535249:AAHEazwEfyCwA7MvHz-XktNyMJojXmgHkf4'
bot = telebot.TeleBot(token=TOKEN)

@bot.message_handler(commands=['start'])
def start(msg):
    chat_id = msg.chat.id
    saludo = "\xF0\x9F\x98\x81 Hola!, puedo ayudarte a obtener informacion relacionada a los recursos del " \
             "sistema operativo de las estaciones de trabajo y servidores de Aircon2100"
    bot.send_message(chat_id, saludo)

@bot.message_handler(commands=['uptime'])
def uptime(msg):
    get_uptime(bot, msg)

@bot.message_handler(commands=['loadavg'])
def uptime(msg):
    get_load(bot, msg)

@bot.message_handler(commands=['memory'])
def uptime(msg):
    get_mem(bot, msg)

if __name__ == '__main__':
    max_loop = 3
    loop = 0
    while 1 and loop <= max_loop:
        try:
            loop += 1
            print("Ejecuntando telegram bot")
            bot.polling(none_stop=True)
        except KeyboardInterrupt:
            print("EJECUCION INTERRUNPIDA")
            break
