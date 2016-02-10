from datetime import timedelta
import time
import paramiko
from utils.helper_functions import do_ssh


def take_snapshot(bot=None, msg=None, remote=None, ssh_user=None, ssh_password=None):
    chat_id = msg.chat.id
    ssh, established = do_ssh(bot, chat_id, remote, ssh_user, ssh_password)
    if established:
        try:
            bot.send_message(chat_id, "He enviado la orden...", parse_mode="Html")
            """channel = ssh.invoke_shell()
            stdin = channel.makefile('wb')
            stdout = channel.makefile('rb')

            stdin.write('''
            export DISPLAY=:0
            /usr/bin/ksnapshot
            exit
            ''')

            print stdout.read()

            stdout.close()
            stdin.close()
            """
            notify = "Se ha jecutado una captura de pantalla en "+ remote+" a peticion de "+msg.chat.first_name +" "+msg.chat.last_name
            broadcast_user_action(bot, chat_id, notify)
            ssh_stdin, stdout, stderr = ssh.exec_command("export DISPLAY=:0 \n /usr/bin/ksnapshot")
            #print stdout.channel.recv_exit_status()
            err = stderr.channel.recv_stderr(1024)
            if err:
                if err.startswith('kbuildsycoca running...'):
                    pass
                else:
                    bot.send_message(chat_id, "	\xF0\x9F\x98\x94 \n %s" % err, parse_mode="Html")
            else:
                bot.send_message(chat_id, "\xF0\x9F\x98\x8E \n<b>Captura de pantalla finalizada en %s</b>" % remote, parse_mode="Html")

        except:
            bot.send_message(chat_id, "\xF0\x9F\x92\xA5 \xF0\x9F\x98\xB5 <b>Ocurrio un inconveniente "
                                          "al solicitar la ejecucion de ksnapshot</b>", parse_mode="Html")
        ssh.close()
    else:
        bot.send_message(chat_id, "	\xF0\x9F\x98\x94 \xF0\x9F\x92\x94 <i>Hijole!, no logre conectar con %s" % remote, parse_mode="Html" )



def broadcast_user_action(bot=None, chat_id=None, info_msg=""):
    bot.send_message(chat_id, "<b>No es que me guste ser chismoso, pero debo hacer publica la orden que me has solicitado para hacerla del conocimiento"
                              "de los integrantes del canal de Estacion Radar Managua</b>", parse_mode="Html")

    bot.send_message('@stecnica', "\xF0\x9F\x93\xA2 <b> %s </b>" % info_msg, parse_mode="Html")