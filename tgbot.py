import logging
import os
from telegram import Updater
from utils.helper_functions import *
from utils.commands_functions import *
from telebot import util

#logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
updater = Updater(token='161535249:AAHEazwEfyCwA7MvHz-XktNyMJojXmgHkf4')
dispatcher = updater.dispatcher
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

start_msg = os.path.join(BASE_DIR, "start_msg.txt")
help_msg = os.path.join(BASE_DIR, "help.txt")


def echo(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text=update.message.text)

def unknown(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="\xF0\x9F\x98\x81 Lo siento, no se que hacer con ese comando.")



def start(bot, msg):
    chat_id=msg.message.chat_id
    large_text = open(start_msg, "rb").read()
    splitted_text = util.split_string(large_text, 3000)
    bot.sendMessage(chat_id, "\xF0\x9F\x98\x81 \xF0\x9F\x91\x8B")
    for text in splitted_text:
        bot.sendMessage(chat_id, text)

def help(bot, msg):
    chat_id = msg.message.chat.id
    large_text = open(help_msg, "rb").read()
    splitted_text = util.split_string(large_text, 3000)
    for text in splitted_text:
        bot.sendMessage(chat_id, text)

def ping(bot, msg):
    chat_id = msg.message.chat.id
    cmd_args = str(msg.message.text).split(" ")[1:]
    if len(cmd_args) > 0:
        for i in range(0,3):
            if(has_ping(cmd_args[0])):
                bot.sendMessage(chat_id, "Respuesta recibida \xF0\x9F\x91\x8D")
            else:
               bot.sendMessage(chat_id, "No hubo respuesta \xF0\x9F\x91\x8E")
    else:
        bot.sendMessage(chat_id, "\xF0\x9F\x98\x8F OK, necesito que me indiques de cual host deseas obtener informacion. "
                                  "Intentalo nuevamente indicando hostname o IP despues del comando")


def system_info(bot, msg):
    chat_id = msg.message.chat.id
    cmd_args = str(msg.message.text).split(" ")[1:]
    if len(cmd_args) > 0:
        get_sys_info(bot, chat_id, cmd_args[0], ssh_user="root", ssh_password="root")
    else:
        bot.sendMessage(chat_id, "\xF0\x9F\x98\x8F OK, necesito que me indiques de cual host deseas obtener informacion. "
                                  "Intentalo nuevamente indicando hostname o IP despues del comando")


def ksnapshot(bot, msg):
    chat_id = msg.message.chat.id
    cmd_args = str(msg.message.text).split(" ")[1:]
    if len(cmd_args) > 0:
        take_snapshot(bot,msg, cmd_args[0], ssh_user="mana", ssh_password="mana")
    else:
        bot.sendMessage(chat_id, "\xF0\x9F\x98\x8F OK, necesito que me indiques de cual host deseas obtener informacion. "
                                  "Intentalo nuevamente indicando hostname o IP despues del comando")



def reboot(bot, msg):
    chat_id = msg.message.chat.id
    cmd_args = str(msg.message.text).split(" ")[1:]
    if len(cmd_args) > 0:
        reboot_host(bot,msg, cmd_args[0], ssh_user="root", ssh_password="root")
    else:
        bot.sendMessage(chat_id, "\xF0\x9F\x98\x8F OK, necesito que me indiques de cual host deseas obtener informacion. "
                                  "Intentalo nuevamente indicando hostname o IP despues del comando")



if __name__ == '__main__':
    dispatcher.addTelegramMessageHandler(echo)
    dispatcher.addUnknownTelegramCommandHandler(unknown)
    dispatcher.addTelegramCommandHandler('start', start)
    dispatcher.addTelegramCommandHandler('help', help)
    dispatcher.addTelegramCommandHandler('sysinfo', system_info)
    dispatcher.addTelegramCommandHandler('snapshot', ksnapshot)
    dispatcher.addTelegramCommandHandler('ping', ping)
    dispatcher.addTelegramCommandHandler('reboot', reboot)

    updater.start_polling()



