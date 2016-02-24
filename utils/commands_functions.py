from datetime import timedelta
import time
import paramiko
from utils.helper_functions import do_ssh


def take_snapshot(bot=None, msg=None, remote=None, ssh_user=None, ssh_password=None):
    chat_id = msg.message.chat.id
    user = msg.message.chat.first_name +" "+msg.message.chat.last_name
    ssh, established = do_ssh(bot, chat_id, remote, ssh_user, ssh_password)
    if established:
        try:
            bot.sendMessage(chat_id, "He enviado la orden...", parse_mode="Html")

            if user is None:
                user = "... no se pudo obtener el nombre"
            notify = "Se ha jecutado una captura de pantalla en "+ remote+" a peticion de " + str(user)
            broadcast_user_action(bot, chat_id, notify)
            ssh_stdin, stdout, stderr = ssh.exec_command("export DISPLAY=:0 \n /usr/bin/ksnapshot")
            #print stdout.channel.recv_exit_status()
            err = stderr.channel.recv_stderr(1024)
            if err:
                if err.startswith('kbuildsycoca running...'):
                    pass
                else:
                    bot.sendMessage(chat_id, "	\xF0\x9F\x98\x94 \n %s" % err, parse_mode="Html")
            else:
                bot.sendMessage(chat_id, "\xF0\x9F\x98\x8E \n<b>Captura de pantalla finalizada en %s</b>" % remote, parse_mode="Html")

        except Exception, e:
            print(e.message)
            bot.sendMessage(chat_id, "\xF0\x9F\x92\xA5 \xF0\x9F\x98\xB5 <b>Ocurrio un inconveniente "
                                          "al solicitar la ejecucion de ksnapshot</b>", parse_mode="Html")
        ssh.close()
    else:
        bot.sendMessage(chat_id, "	\xF0\x9F\x98\x94 \xF0\x9F\x92\x94 <i>Hijole!, no logre conectar con %s" % remote, parse_mode="Html" )



def reboot_host(bot=None, msg=None, remote=None, ssh_user=None, ssh_password=None):
    chat_id = msg.message.chat.id
    user = msg.message.chat.first_name +" "+msg.message.chat.last_name
    ssh, established = do_ssh(bot, chat_id, remote, ssh_user, ssh_password)
    if established:
        try:
            bot.sendMessage(chat_id, "He enviado la orden...", parse_mode="Html")

            if user is None:
                user = "... no se pudo obtener el nombre"
            notify = "Se ha mandado a reiniciar "+ remote+" a peticion de " + str(user)
            broadcast_user_action(bot, chat_id, notify)
            ssh_stdin, stdout, stderr = ssh.exec_command("init 6")
            #print stdout.channel.recv_exit_status()
            err = stderr.channel.recv_stderr(1024)
            if err:
                if err.startswith('kbuildsycoca running...'):
                    pass
                else:
                    bot.sendMessage(chat_id, "	\xF0\x9F\x98\x94 \n %s" % err, parse_mode="Html")
            else:
                bot.sendMessage(chat_id, "\xF0\x9F\x98\x8E \n<b>%s se ha o se esta reiniciando</b>" % remote, parse_mode="Html")

        except Exception, e:
            print(e.message)
            bot.sendMessage(chat_id, "\xF0\x9F\x92\xA5 \xF0\x9F\x98\xB5 <b>Ocurrio un inconveniente "
                                          "al solicitar el reinicio</b>", parse_mode="Html")
        ssh.close()
    else:
        bot.sendMessage(chat_id, "	\xF0\x9F\x98\x94 \xF0\x9F\x92\x94 <i>Hijole!, no logre conectar con %s" % remote, parse_mode="Html" )



def broadcast_user_action(bot=None, chat_id=None, info_msg=""):
    bot.sendMessage(chat_id, " \xF0\x9F\x91\xBC <b>Accion publicada en canal @stecnica</b>", parse_mode="Html")
    bot.sendMessage('@stecnica', "\xF0\x9F\x93\xA2 \xF0\x9F\x91\xBC <b> %s </b>" % info_msg, parse_mode="Html")