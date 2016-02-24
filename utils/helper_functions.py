from datetime import timedelta
import datetime
import subprocess
import socket, struct
import time
import paramiko

def clear_multiple_spaces(text=""):
    return ' '.join(text.split())

def has_ping(host):
    try:
        output =  subprocess.call("ping -c 1 %s" % host,
                              shell=True,
                              stdout=open('/dev/null', 'w'),
                              stderr=subprocess.STDOUT)
        if output == 0:
            return True
        else:
            return False
    except Exception, e:
        return False



def do_ssh(bot=None, chat_id=None, remote=None, ssh_user=None, ssh_password=None):
    bot.sendMessage(chat_id, "\xF0\x9F\x98\x8C Verificando si <b>"+ remote +"</b> esta accesible"
                     , parse_mode="Html")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    if has_ping(remote):
        bot.sendMessage(chat_id, "\xE2\x9C\x8C \xF0\x9F\x8E\x89 \xF0\x9F\x8E\x8A 	\xF0\x9F\x91\x8F \n"
                                  "Muy bien permiteme un momento...")
        conn = False
        i = 0
        while 1 and i < 3:
            try:
                ssh.connect(remote, username=ssh_user, password=ssh_password)
                return ssh, True
                break
            except paramiko.AuthenticationException:
                bot.sendMessage(chat_id, "\xF0\x9F\x98\xA8 \xF0\x9F\x91\xAE Fallo la autenticacion al conectarse a: %s" % remote)
                break
            except Exception, e:
                face_str = "\xF0\x9F\x98\xAC"
                if i == 1:
                    face_str = "\xF0\x9F\x98\xB3"
                elif i == 2:
                    face_str="\xF0\x9F\x98\xB0"
                bot.sendMessage(chat_id, face_str +"<i> No pude establecer conexion con el destino \n"
                                          "\xF0\x9F\x98\x87 Intentare una vez mas </i>", parse_mode="Html")
                i += 1
                time.sleep(2)
            if i >=3:
                bot.sendMessage(chat_id, "	\xF0\x9F\x98\x94 \xF0\x9F\x92\x94 <i>Hijole!, hice lo posible, pero no me fue posible "
                                          "conectar con: %s, no hubo quimica entre nosotros </i> \xF0\x9F\x98\x85" % remote, parse_mode="Html" )
        return  ssh, conn


    else:
        bot.sendMessage(chat_id, "\xF0\x9F\x98\xB2 \xE2\x9D\x8C \xF0\x9F\x92\x80"
                                  " Vaya!... parece que no podemos comunicarnos con %s" % remote
                         , parse_mode="Html")
        return ssh, False


def get_sys_info(bot=None, chat_id=None, remote=None, ssh_user=None, ssh_password=None):
    ssh, conn = do_ssh(bot, chat_id, remote, ssh_user, ssh_password)
    print(conn)
    if conn:
        get_uptime_stat(ssh, bot, chat_id)
        get_load_avg(ssh, bot, chat_id)
        get_cpu_usage(ssh, bot, chat_id)
        get_disk_usage(ssh, bot, chat_id)
        get_syncronization_stat(ssh, bot, chat_id)
        get_mem_stat(ssh, bot, chat_id)
        ssh.close()
    else:
        bot.sendMessage(chat_id, "	\xF0\x9F\x98\x94 \xF0\x9F\x92\x94 <i>Hijole!, no logre conectar con %s"
                         % remote, parse_mode="Html" )



def get_load_avg(ssh=None, bot=None, chat_id=None):
    try:
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
        bot.sendMessage(chat_id, "\xF0\x9F\x98\x8E <b>Carga primedio: %s </b>"
                                     % str_lavg, parse_mode="Html")
        bot.sendMessage(chat_id, "\xF0\x9F\x98\x8E <b>Procesos: %s </b>" % procs, parse_mode="Html")
    except:
        bot.sendMessage(chat_id, "\xF0\x9F\x92\xA5 \xF0\x9F\x98\xB5 <b>Ocurrio un inconveniente "
                                  "al solicitar la carga promedio</b>", parse_mode="Html")


def get_mem_stat(ssh=None, bot=None, chat_id=None):
    try:
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
        str_swap = "\n-----SWAP-----\nTotal: "+swap[1]+" MB  \nUsado: "+ swap[2] + " MB   \nLibre: "+ swap[3]+" MB"
        str_ram += str_swap
        bot.sendMessage(chat_id, "\xF0\x9F\x98\x8E \n<b>-----RAM----- %s </b>"
                                 % str_ram, parse_mode="Html")
    except:
        bot.sendMessage(chat_id, "\xF0\x9F\x92\xA5 \xF0\x9F\x98\xB5 <b>Ocurrio un inconveniente "
                                  "al solicitar el uso de memoria</b>", parse_mode="Html")

def get_uptime_stat(ssh=None, bot=None, chat_id=None):
    try:
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("cat /proc/uptime")
        values = []
        for i, line in enumerate(ssh_stdout):
            line = line.rstrip()
            line = line.rstrip('\n').rstrip('\r').strip()
            line = clear_multiple_spaces(line)
            values.append(line)
        uptime_seconds = float(str(values[0]).split()[0])
        uptime_string = str(timedelta(seconds = uptime_seconds))
        bot.sendMessage(chat_id, "\xF0\x9F\x98\x8E <b>Uptime: %s</b> " % uptime_string.split('.')[0], parse_mode="Html")
    except:
        bot.sendMessage(chat_id, "\xF0\x9F\x92\xA5 \xF0\x9F\x98\xB5 <b>Ocurrio un inconveniente "
                                  "al solicitar tiempo de ejecucion</b>", parse_mode="Html")



def get_cpu_usage(ssh=None, bot=None, chat_id=None):
    try:
        stdin, stdout, stderr = ssh.exec_command("mpstat")
        values = []
        for i, line in enumerate(stdout):
            line = line.rstrip()
            line = line.rstrip('\n').rstrip('\r').strip()
            line = clear_multiple_spaces(line)
            values.append(line)

        splited = str(values[3]).split()
        usage = 100 - float(splited[len(splited)-2])
        usage_str = "{0:.2f}".format(usage)+"%"
        bot.sendMessage(chat_id, "\xF0\x9F\x98\x8E <b>Uso de CPU: %s</b> " % usage_str, parse_mode="Html")
    except Exception, e:
        print(e.message)
        bot.sendMessage(chat_id, "\xF0\x9F\x92\xA5 \xF0\x9F\x98\xB5 <b>Ocurrio un inconveniente "
                                  "al solicitar el uso de cpu</b>", parse_mode="Html")


def get_disk_usage(ssh=None, bot=None, chat_id=None):
    try:
        # Send the command (non-blocking)
        stdin, stdout, stderr = ssh.exec_command("df -hT /")

        # Wait for the command to terminate
        values = []
        for i, line in enumerate(stdout):
            line = line.rstrip()
            line = line.rstrip('\n').rstrip('\r').strip()
            line = clear_multiple_spaces(line)
            values.append(line)

        splited = str(values[2]).split()
        percent = splited[len(splited)-2]
        bot.sendMessage(chat_id, "\xF0\x9F\x98\x8E <b>Uso de disco particion /: %s</b> " % percent, parse_mode="Html")
    except Exception, e:
        print(e.message)
        bot.sendMessage(chat_id, "\xF0\x9F\x92\xA5 \xF0\x9F\x98\xB5 <b>Ocurrio un inconveniente "
                                  "al solicitar el uso de disco</b>", parse_mode="Html")


def get_syncronization_stat(ssh=None, bot=None, chat_id=None):
    try:
        stdin, stdout, stderr = ssh.exec_command("date '+%Y-%m-%d %H:%M:%S %Z'")
        # Wait for the command to terminate
        values = []
        for i, line in enumerate(stdout):
            line = line.rstrip()
            line = line.rstrip('\n').rstrip('\r').strip()
            line = clear_multiple_spaces(line)
            values.append(line)
        local = datetime.datetime.strptime(values[0],'%Y-%m-%d %H:%M:%S %Z')
        sntp_time =  get_ntp_time()
        dif = local - sntp_time
        sec = dif.total_seconds()
        offset = str(sec)
        bot.sendMessage(chat_id, "\xF0\x9F\x98\x8E <b>Diferencia respecto al servidor NTP: %s seg</b> " % offset, parse_mode="Html")
    except Exception, e:
        print(e.message)
        bot.sendMessage(chat_id, "\xF0\x9F\x92\xA5 \xF0\x9F\x98\xB5 <b>Ocurrio un inconveniente "
                                  "al verificar sincronia con servidor NTP</b>", parse_mode="Html")




#Obtener hora del servidor ntp
def get_ntp_time():
    TIME1970 = 2208988800L
    # Thanks to F.Lundh
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.settimeout(2)
    address = "10.160.80.205"
    data = '\x1b' + 47 * '\0'
    client.sendto(data, (address, 123))
    try:
        data, address = client.recvfrom(1024)
        if data:
            t = struct.unpack('!12I', data)[10]
            t -= TIME1970
            utc_dt = datetime.datetime.utcfromtimestamp(t)
            return utc_dt
        else:
            print 'No Response received from:', address
    except socket.timeout:
        print 'No Response received from NTP'