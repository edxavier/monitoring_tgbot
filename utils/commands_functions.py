from datetime import timedelta
import time
import paramiko
from utils.helper_functions import do_ssh


def take_snapshot(bot=None, chat_id=None, remote=None, ssh_user=None, ssh_password=None):
    ssh, established = do_ssh(bot, chat_id, remote, ssh_user, ssh_password)
    if established:
        try:
            ssh_stdin, stdout, ssh_stderr = ssh.exec_command("/usr/bin/ksnapshot")
            print stdout.channel.recv_exit_status()
            if stdout.channel.recv_exit_status()==0:
                bot.send_message(chat_id, "\xF0\x9F\x98\x8E \n<b>He enviado la orden verifica por favor</b>", parse_mode="Html")
            else:
                bot.send_message(chat_id, "	\xF0\x9F\x98\x94 \n<b>Lo siento no se pudo ejecutar la orden</b>", parse_mode="Html")
        except:
            bot.send_message(chat_id, "\xF0\x9F\x92\xA5 \xF0\x9F\x98\xB5 <b>Ocurrio un inconveniente "
                                          "al solicitar el uso de memoria</b>", parse_mode="Html")
        ssh.close()
    else:
        bot.send_message(chat_id, "	\xF0\x9F\x98\x94 \xF0\x9F\x92\x94 <i>Hijole!, no logre conectar con %s" % remote, parse_mode="Html" )

