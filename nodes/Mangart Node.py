import socket
import threading
import json
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

def cross():
    global ip_table
    while True:
        data, address = sock.recvfrom(1024)
        data = data.decode()
        data = json.loads(data)

        if(len(ip_table) > len(data)):
            for i in range(len(data)):
                if(ip_table[i] != data[i]):
                    ip_table[len(ip_table)] = data[i]
        if(len(data) > len(ip_table)):
            for i in range(len(ip_table)):
                if(ip_table[i] != data[i]):
                    ip_table[len(ip_table)] = data[i]
                
def send_cross():
    global ip_table
    while True:
        for i in range(0,len(verif)-1):
            dtd = json.dumps(ip_table)
            server_socket.sendto(dtd.encode(), (str(verif[i]),24339))
    
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
        server_socket.sendto(ip_table_enc.encode(), address)

b = threading.Thread(name='background', target=background)
b.start()

x = threading.Thread(name='cross', target=cross)
x.start()

vv = threading.Thread(name='send_cross', target=send_cross)
vv.start()
