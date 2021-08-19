import socket
import threading
import json
import time
import configparser
import pickle

try:
    open("ip_table.db","rb").close()

except FileNotFoundError:
    dest = open("ip_table.db", "wb")
    rv = {}
    dtd_enc = pickle.dumps(rv)
    pickle.dump(dtd_enc, dest)
    dest.close()

class table:
    def writes(tbl):
        dest = open("ip_table.db", "wb")
        tbl_enc = pickle.dumps(tbl)
        pickle.dump(tbl_enc, dest)
        dest.close()
    
    def reads():
        try:
            dest = open("ip_table.db", "rb")
            dtd_enc = pickle.load(dest)
            tbl = pickle.loads(dtd_enc)
            dest.close()
            return tbl
        except:
            return {}

config = configparser.ConfigParser()
config.read('node.json')

ip1 = config['verif']['ip']
ip2 = config['verif']['ip 2']
ip3 = config['verif']['ip 3']
ip4 = config['verif']['ip 4']

verif = []

verif.append(ip1)
verif.append(ip2)
verif.append(ip3)
verif.append(ip4)

print(verif)

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

local_ip = get_ip_address()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('', 18000))

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 24339))

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(1.0)

echo_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   
def rec_ip_tbl():
    while(True):
        ip_table = table.reads()
        data_enc, address = sock.recvfrom(1024)
        data = data_enc.decode()
        data = json.loads(data)

        if(len(data) > len(ip_table) or len(data) == len(ip_table)):
            for i in range(len(ip_table)-1):
                try:
                    if(ip_table[i] != data[i]):
                        ip_table[data[i][1]] = data[i][0]
                except:
                    pass
        elif(len(data) > len(ip_table)-1):
            for i in range(len(data)):
                try:
                    if(ip_table[i] != data[i]):
                        ip_table[data[i][1]] = data[i][0]
                except:
                    pass
        table.writes(ip_table)
        time.sleep(3)

def snd_ip_tbl():
    while(True):
        ip_table = table.reads()
        ip_table_enc = json.dumps(ip_table)
        for i in range(len(verif)):
            client_socket.sendto(ip_table_enc.encode(),(str(verif[i]), 24339))
        time.sleep(2)

def background():
    while True:
        ip_table = table.reads()
        data, address = server_socket.recvfrom(1024)
        x = data.decode()
        x = x.strip("[]")
        x = x.replace("'","")
        x = x.replace(" ","")
        dt = x.split(',')
        try:
            ip_table[dt[1]]
        except KeyError:
            print("Connected with " + dt[0])
        ip_table[dt[1]] = dt[0]
        ip_table_enc = json.dumps(ip_table)
        server_socket.sendto(ip_table_enc.encode(),(str(dt[0]), 9000))
        table.writes(ip_table)
        time.sleep(3)

def delt():
    while(True):
        ip_table = table.reads()
        for i in range(len(ip_table)):
            ip_table = table.reads()
            ip_addr = list(ip_table.values())[i]
            echo_address = (str(ip_addr),9000)
            try:
                echo_socket.connect((echo_address))
                echo_socket.send("HEY?".encode())
                print("ok")
                table.writes(ip_table)
            except ConnectionRefusedError:
                 print("Removed: " + str(ip_addr))
                 sv = list(ip_table.keys())
                 idx = sv[i]
                 ip_table.pop(idx)
                 table.writes(ip_table)
                 break
            time.sleep(2)
            print(ip_table)
    print("x")


bg = threading.Thread(name='background', target=background)
bg.start()

recip = threading.Thread(name='REC_IP', target=rec_ip_tbl)
recip.start()

sndip = threading.Thread(name='SND_IP', target=snd_ip_tbl)
sndip.start()

delen = threading.Thread(name='delen', target=delt)
delen.start()