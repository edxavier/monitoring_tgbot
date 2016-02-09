from datetime import timedelta
import time
import paramiko

def clear_multiple_spaces(text=""):
    return ' '.join(text.split())

def get_uptime(bot, msg):
    chat_id = msg.chat.id
    cmd_args = str(msg.text).split(" ")[1:]
    if len(cmd_args) > 0:
        bot.send_message(chat_id, "\xF0\x9F\x98\x8C OK, ya te averiguo el uptime para:  <b>"+ cmd_args[0]+"</b>" , parse_mode="Html")
        i = 0
        while 1 and i < 3:
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(cmd_args[0], username="server", password="server")
                ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("cat /proc/uptime")
                values = []
                for i, line in enumerate(ssh_stdout):
                    line = line.rstrip()
                    line = line.rstrip('\n').rstrip('\r').strip()
                    line = clear_multiple_spaces(line)
                    values.append(line)
                uptime_seconds = float(str(values[0]).split()[0])
                uptime_string = str(timedelta(seconds = uptime_seconds))
                bot.send_message(chat_id, "\xF0\x9F\x98\x8E <b>Uptime: %s</b> " % uptime_string.split('.')[0], parse_mode="Html")
                ssh.close()
                break
            except paramiko.AuthenticationException:
                bot.send_message(chat_id, "\xF0\x9F\x98\xA8 Fallo la autenticacion al conectarse a: %s" % cmd_args[0])
                break
            except Exception, e:
                face_str = "\xF0\x9F\x98\xAC"
                if i == 1:
                    face_str = "\xF0\x9F\x98\xB3"
                elif i == 2:
                    face_str="\xF0\x9F\x98\xB0"
                bot.send_message(chat_id, face_str +"<i> No pude establecer conexion SSH \n"
                                          "\xF0\x9F\x98\x87 Intentare una vez mas </i>", parse_mode="Html")
                i += 1
                time.sleep(2)
            if i >=3:
                bot.send_message(chat_id, "	\xF0\x9F\x98\x94 <i>Hijole!, hice lo posible, pero no me fue posible "
                                          "conectar con: %s </i>" % cmd_args[0], parse_mode="Html" )

    else:
        bot.send_message(chat_id, "\xF0\x9F\x98\x8F OK, necesito que me indiques de que host deseas obtener infirmacion\n"
                                  "Por ejemplo: <</uptime servidor1>>, intentalo nuevamente"
                                  " indicando hostname o IP despues del comando")


def get_load(bot, msg):
    chat_id = msg.chat.id
    cmd_args = str(msg.text).split(" ")[1:]
    if len(cmd_args) > 0:
        bot.send_message(chat_id, "\xF0\x9F\x98\x8C OK, carga promedio  para:  <b>"+ cmd_args[0]+"</b>" , parse_mode="Html")
        i = 0
        while 1 and i < 3:
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(cmd_args[0], username="server", password="server")
                ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("cat /proc/loadavg")
                values = []
                for j, line in enumerate(ssh_stdout):
                    line = line.rstrip()
                    line = line.rstrip('\n').rstrip('\r').strip()
                    line = clear_multiple_spaces(line)
                    values.append(line)
                splited = str(values[0]).split()
                load_avg = (float(splited[0])+float(splited[1])+float(splited[2])/3)
                procs = splited[3]
                #str_lavg = "{0:.2f}".format(load_avg)
                str_lavg = splited[0]+"    "+splited[1]+"    "+splited[2]
                bot.send_message(chat_id, "\xF0\x9F\x98\x8E <b>Loadavg: %s </b>"
                                 % str_lavg, parse_mode="Html")
                bot.send_message(chat_id, "\xF0\x9F\x98\x8E <b>Procesos: %s </b>" % procs, parse_mode="Html")
                ssh.close()
                break
            except paramiko.AuthenticationException:
                bot.send_message(chat_id, "\xF0\x9F\x98\xA8 Fallo la autenticacion al conectarse a: %s" % cmd_args[0])
                break
            except Exception, e:
                face_str = "\xF0\x9F\x98\xAC"
                if i == 1:
                    face_str = "\xF0\x9F\x98\xB3"
                elif i == 2:
                    face_str="\xF0\x9F\x98\xB0"
                bot.send_message(chat_id, face_str +"<i> No pude establecer conexion SSH \n"
                                          "\xF0\x9F\x98\x87 Intentare una vez mas </i>", parse_mode="Html")
                i += 1
                time.sleep(2)
            if i >=3:
                bot.send_message(chat_id, "\xF0\x9F\x98\x94 <i>Hijole!, hice lo posible, pero no me fue posible "
                                          "conectar con: %s </i>" % cmd_args[0], parse_mode="Html" )

    else:
        bot.send_message(chat_id, "\xF0\x9F\x98\x8F OK, necesito que me indiques de que host deseas obtener infirmacion\n"
                                  "Por ejemplo: <</uptime servidor1>>, intentalo nuevamente"
                                  " indicando hostname o IP despues del comando")


def get_mem(bot, msg):
    chat_id = msg.chat.id
    cmd_args = str(msg.text).split(" ")[1:]
    if len(cmd_args) > 0:
        bot.send_message(chat_id, "\xF0\x9F\x98\x8C OK, estado de memoria para:  <b>"+ cmd_args[0]+"</b>" , parse_mode="Html")
        i = 0
        while 1 and i < 3:
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(cmd_args[0], username="server", password="server")
                ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("free -m")
                # Wait for the command to terminate
                values = []
                for i, line in enumerate(ssh_stdout):
                    if i <= 3:
                        line = line.rstrip()
                        line = line.rstrip('\n').rstrip('\r').strip()
                        line = clear_multiple_spaces(line)
                        values.append(line)
                ram = str(values[1]).split()
                swap = str(values[3]).split()

                free_ram_percent = (float(ram[3]) / float(ram[1])) * 100
                str_ram = "\nTotal: "+ram[1]+" MB  \nUsado: "+ ram[2] + " MB   \nLibre: "+ ram[3]+ \
                          " MB ("+"{0:.2f}".format(free_ram_percent)+" %)"
                str_swap = "\n---SWAP---\nTotal: "+swap[1]+" MB  \nUsado: "+ swap[2] + " MB   \nLibre: "+ swap[3]+" MB"
                str_ram += str_swap
                bot.send_message(chat_id, "\xF0\x9F\x98\x8E \n<b>---RAM--- %s </b>"
                                 % str_ram, parse_mode="Html")
                ssh.close()
                break
            except paramiko.AuthenticationException:
                bot.send_message(chat_id, "\xF0\x9F\x98\xA8 Fallo la autenticacion al conectarse a: %s" % cmd_args[0])
                break
            except Exception, e:
                face_str = "\xF0\x9F\x98\xAC"
                if i == 1:
                    face_str = "\xF0\x9F\x98\xB3"
                elif i == 2:
                    face_str="\xF0\x9F\x98\xB0"
                bot.send_message(chat_id, face_str +"<i> No pude establecer conexion SSH \n"
                                          "\xF0\x9F\x98\x87 Intentare una vez mas </i>", parse_mode="Html")
                i += 1
                time.sleep(2)
            if i >=3:
                bot.send_message(chat_id, "\xF0\x9F\x98\x94 <i>Hijole!, hice lo posible, pero no me fue posible "
                                          "conectar con: %s </i>" % cmd_args[0], parse_mode="Html" )

    else:
        bot.send_message(chat_id, "\xF0\x9F\x98\x8F OK, necesito que me indiques de que host deseas obtener infirmacion\n"
                                  "Por ejemplo: <</uptime servidor1>>, intentalo nuevamente"
                                  " indicando hostname o IP despues del comando")
