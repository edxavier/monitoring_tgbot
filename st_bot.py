__author__ = 'edx'
from utils.helper_functions import *
from utils.commands_functions import *
import telebot
from telebot import util

TOKEN = '161535249:AAHEazwEfyCwA7MvHz-XktNyMJojXmgHkf4'
bot = telebot.TeleBot(token=TOKEN)

@bot.message_handler(commands=['start'])
def start(msg):
    chat_id = msg.chat.id
    large_text = open("start_msg.txt", "rb").read()
    splitted_text = util.split_string(large_text, 3000)
    bot.send_message(chat_id, "\xF0\x9F\x98\x81 \xF0\x9F\x91\x8B")
    for text in splitted_text:
        bot.send_message(chat_id, text)

@bot.message_handler(commands=['help'])
def help(msg):
    chat_id = msg.chat.id
    large_text = open("help.txt", "rb").read()
    splitted_text = util.split_string(large_text, 3000)
    print(msg)
    #for text in splitted_text:
     #   bot.send_message(chat_id, text)


@bot.message_handler(commands=['ping'])
def ping(msg):
    chat_id = msg.chat.id
    cmd_args = str(msg.text).split(" ")[1:]
    if len(cmd_args) > 0:
        for i in range(0,3):
            if(has_ping(cmd_args[0])):
                bot.send_message(chat_id, "Respuesta recibida \xF0\x9F\x91\x8D")
            else:
               bot.send_message(chat_id, "No hubo respuesta \xF0\x9F\x91\x8E")
    else:
        bot.send_message(chat_id, "\xF0\x9F\x98\x8F OK, necesito que me indiques de cual host deseas obtener informacion. "
                                  "Intentalo nuevamente indicando hostname o IP despues del comando")

@bot.message_handler(commands=['sysinfo'])
def system_info(msg):
    chat_id = msg.chat.id
    cmd_args = str(msg.text).split(" ")[1:]
    if len(cmd_args) > 0:
        get_sys_info(bot, chat_id, cmd_args[0], ssh_user="server", ssh_password="server")
    else:
        bot.send_message(chat_id, "\xF0\x9F\x98\x8F OK, necesito que me indiques de cual host deseas obtener informacion. "
                                  "Intentalo nuevamente indicando hostname o IP despues del comando")

@bot.message_handler(commands=['ksnapshot'])
def ksnapshot(msg):
    chat_id = msg.chat.id
    cmd_args = str(msg.text).split(" ")[1:]
    if len(cmd_args) > 0:
        take_snapshot(bot,msg, cmd_args[0], ssh_user="server", ssh_password="server")
    else:
        bot.send_message(chat_id, "\xF0\x9F\x98\x8F OK, necesito que me indiques de cual host deseas obtener informacion. "
                                  "Intentalo nuevamente indicando hostname o IP despues del comando")



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
