#---------------------------------#
#-        NAT-Coin v1.0.0        -#
#-   Copyright Dima Galkin 2021  -#
#---------------------------------#


# Below the program checks that all the requiered modules are installed and if not the user is requestes to install it

try:
    import socket
except:
    print("Socket Is Not Instaled Please Install It.")
    input("Press any key to exit.")
    exit()

try:
    import threading
except:
    print("Threading Is Not Instaled Please Install It.")
    input("Press any key to exit.")
    exit()

try:
    import json
except:
    print("Json Is Not Instaled Please Install It.")
    input("Press any key to exit.")
    exit()

try:
    import time
except:
    print("Time Is Not Instaled Please Install It.")
    input("Press any key to exit.")
    exit()

try:
    import configparser
except:
    print("Configparser Is Not Instaled Please Install It.")
    input("Press any key to exit.")
    exit()

try:
    import pickle
except:
    print("Pickle Is Not Instaled Please Install It.")
    input("Press any key to exit.")
    exit()

# define registered user table
regtable = []

# location of the ip addresses
ip_file = "ip_table.db"

# see if the file exists
try:
    open(ip_file,"rb").close()

# if not we create it 
except FileNotFoundError:
    dest = open(ip_file, "wb")
    rv = {}
    dtd_enc = pickle.dumps(rv)
    pickle.dump(dtd_enc, dest)
    dest.close()

# class for working fith the ip_table file
class table:
    # write to the file
    def writes(tbl):
        dest = open(ip_file, "wb")
        tbl_enc = pickle.dumps(tbl)
        pickle.dump(tbl_enc, dest)
        dest.close()
    # read from the file
    def reads():
        try:
            dest = open(ip_file, "rb")
            dtd_enc = pickle.load(dest)
            tbl = pickle.loads(dtd_enc)
            dest.close()
            return tbl
        except:
            return {}

# read from the node ip conf file
config = configparser.ConfigParser()
config.read('node.json')

# load the ip addresses
ip1 = config['verif']['ip1']
ip2 = config['verif']['ip2']
ip3 = config['verif']['ip3']
ip4 = config['verif']['ip4']

# add the adresses to the te verif list

verif = []

# append to the verify list if it is not 0
def app(ver):
    if(ver != 0):
        verif.append(ver)

# append the ip addresses
app(ip1)
app(ip2)
app(ip3)
app(ip4)


print(verif)

# define the diffrent sockets
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('', 18000))

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 24339))

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(1.0)

echo_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# function for receiving an iptable
def rec_ip_tbl():
    while(True):
        # read the table
        ip_table = table.reads()
        # recive the iptable from another node
        data_enc, address = sock.recvfrom(1024)
        data = data_enc.decode()
        data = json.loads(data)

        # compare the data
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

# send the ip table to a node
def snd_ip_tbl():
    while(True):
        ip_table = table.reads()
        ip_table_enc = json.dumps(ip_table)
        for i in range(len(verif)):
            # send the table to the socket
            client_socket.sendto(ip_table_enc.encode(),(str(verif[i]), 24339))
        time.sleep(1)

def background():
    while True:
        # recive the data
        time.sleep(2.5)
        data, address = server_socket.recvfrom(1024)
        ip_table = table.reads()
        # process the data
        x = data.decode()
        x = x.strip("[]")
        x = x.replace("'","")
        x = x.replace(" ","")
        dt = x.split(',')
        # see if the the client is not all ready connected
        if(dt[0] in ip_table.values()):
            pass
        else:
            # print connectin status
            print("Connected with " + dt[0])
            # append to the ip table
            ip_table[dt[1]] = dt[0]
            table.writes(ip_table)

        ip_table_enc = json.dumps(ip_table)
        # one proceced send the table back to the client
        server_socket.sendto(ip_table_enc.encode(),(str(dt[0]), 9000))

# this deletes inactive ip adresses from the tables
def delt():
    i = 0
    while(True):
        # load the table
        ip_table = table.reads()
        try:
            # set the destination address
            ip_addr = list(ip_table.values())[i]
            echo_address = (str(ip_addr),9000)
            try:
                # check if the client is alive
                echo_socket.connect((echo_address))
                echo_socket.send("HEY?".encode())
                time.sleep(0.5)
            except ConnectionRefusedError:
                    # if the client is not respondin remove it
                    print("Removed: " + str(ip_addr))
                    ip_table = table.reads()
                    # get the value by index
                    sv = list(ip_table.keys())
                    idx = sv[i]
                    # remove it from the table
                    ip_table.pop(idx)
                    table.writes(ip_table)
                    i -= 1
                    time.sleep(0.5)
            # set i to 0 if this is the last element in the loop
            if((i + 1) > (len(ip_table) - 1)):
                i = 0
            else:
                i += 1
        except IndexError:
            continue
        time.sleep(0.5)

# define and start threads
bg = threading.Thread(name='background', target=background)
bg.start()

recip = threading.Thread(name='REC_IP', target=rec_ip_tbl)
recip.start()

sndip = threading.Thread(name='SND_IP', target=snd_ip_tbl)
sndip.start()

delen = threading.Thread(name='delen', target=delt)
delen.start()