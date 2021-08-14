import socket
import threading
import json
import time
import configparser

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
global ip_table

ip_table = {}

local_ip = get_ip_address()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('', 18000))

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 24339))

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(1.0)
   
def rec_ip_tbl():
    global ip_table
    while(True):
        data_enc, address = sock.recvfrom(1024)
        data = data_enc.decode()
        data = json.loads(data)
        print(data)

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
        
        print(ip_table)

def snd_ip_tbl():
    global ip_table
    while(True):
        ip_table_enc = json.dumps(ip_table)
        for i in range(len(verif)):
            client_socket.sendto(ip_table_enc.encode(),(str(verif[i]), 24339))
        time.sleep(2)

def background():
    global ip_table
    while True:
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
        time.sleep(2)

def delete_ip():
    global ip_table
    alive = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while(True):
        for i in range(len(ip_table)):
            try:
                alive.connect(ip_table[i][1], 9000)
                print(ip_table[i][1])
                alive.send("HEY!")
            except:
                del ip_table[i]

bg = threading.Thread(name='background', target=background)
bg.start()

recip = threading.Thread(name='REC_IP', target=rec_ip_tbl)
recip.start()

sndip = threading.Thread(name='SND_IP', target=snd_ip_tbl)
sndip.start()

rt = threading.Thread(name='rst', target=delete_ip)
rt.start()