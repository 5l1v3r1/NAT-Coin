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
    import time
    from time import sleep
    from time import time
except:
    print("Time Is Not Instaled Please Install It.")
    input("Press any key to exit.")
    exit()

try:
    import random
except:
    print("Random Is Not Instaled Please Install It.")
    input("Press any key to exit.")
    exit()

try:
    import getpass
except:
    print("GetPass Is Not Instaled Please Install It.")
    input("Press any key to exit.")
    exit()

try:
    import configparser
except:
    print("Configparser Is Not Instaled Please Install It.")
    input("Press any key to exit.")
    exit()

try:
    from subprocess import call
except:
    print("Subprocess Is Not Instaled Please Install It.")
    input("Press any key to exit.")
    exit()

try:
    import os
except:
    print("OS Is Not Instaled Please Install It.")
    input("Press any key to exit.")
    exit()

try:
    import json
except:
    print("Json Is Not Instaled Please Install It.")
    input("Press any key to exit.")
    exit()

try:
    import hashlib
except:
    print("Hashlib Is Not Instaled Please Install It.")
    input("Press any key to exit.")
    exit()

try:
    import atexit
except:
    print("Atexit Is Not Instaled Please Install It.")
    input("Press any key to exit.")
    exit()

def save_callback(sender, data):
    print("Save Clicked")

# read the node ip conf file
nfile = open("node.json","r")
nodes = nfile.read()
nodes = json.loads(nodes)
nfile.close()

# We define our global variables
global res_addr, addr

# We define where all of the ip adresses will be stored

addr ={}

# --------The Blockchain--------

# Create the blockchain class

class Blockchain(object):
    # init function
    def __init__(self):
        # create the chain
        self.chain = []
        # create the pending transatcion array
        self.pending_transactions = []
        # Make our first block
        self.new_block(previous_hash="the begining",proof=100)

    # How we make a new block
    def new_block(self, proof, previous_hash=None):
        # Make our block
        block = {
            # What goes into our block
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.pending_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        # reset the pending transaction as we have included them in our block
        self.pending_transactions = []
        # Add the block to the chain!
        self.chain.append(block)
        
        return block

    @property

    # This function returns the lat block in the chain
    def last_block(self):

        return self.chain[-1]

    # Get the block 'num' from the end of the chain
    def num_block(self,num):
        # if we didnt take away from 0 we would get the block 'num' from the start of the chain and not from the end
        num = 0 - num
        # get and return the block
        return self.chain[num]

    # this is how we created a new transaction ad later append it the pending transactions
    def new_transaction(self, sender, recipient, amount,balance):
        # define what goes into our transaction dict
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
            'balance' : balance
        }
        # append it to pending transactions
        self.pending_transactions.append(transaction)
        
        # return the last block
        return self.last_block['index'] + 1

    # how we hash our block
    def hash(self,block):
        string_object = json.dumps(block, sort_keys=True)
        block_string = string_object.encode()

        raw_hash = hashlib.sha256(block_string)
        hex_hash = raw_hash.hexdigest()

        return hex_hash

    # how we create a block from a transaction
    def save(self,to,fro,amm,balance):
        # create a new recent trasnaction
        blockchain.new_transaction(to,fro,amm,balance)
        # create a new block and clear recent transactions
        blockchain.new_block(12345)
        # open and write to the blockchain file
        f = open("nat.blockchain",'w')
        f.write(json.dumps(blockchain.chain))
        f.close()
        
# define blockchain
blockchain = Blockchain()

# a function which can read and pull things from the blockchain
def get_from_blockchain(what,num):
    # this checks if the option for which block was set to most recent
    if num == 'most_rec':
        # define the most recent block number
        num = len(blockchain.chain) - 1
    else:
        # make the number a negative so it counts from the end of the blockchain.
        num = 0 - num
    try:
        # try to pull from the blockchain but is it is blank it returns blank
        action = blockchain.chain[num]
        transaction = action['transactions']
        transaction = transaction[0]
        return transaction[what]
    except:
        return 'blank'

# this function gets our ip address
def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("1.1.1.1", 80))
        return s.getsockname()[0]
    except OSError:
        print("No Network Connection Avalible")

#create all of our sockets

#server socket for reciving data
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('', 9000))

#client socket for sending data
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(1.0)

# this socket is contacted to see if the client is still online
echo_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# what to do when the program is exited
def exit_handler():
    # clos the server socket
    server_socket.close()
    # say it has shutdown
    print("NAT-Coin Wallet Has Shutdown")

# start the function above 
atexit.register(exit_handler)

# this is where we find an avalible node to connect to
def findNode():
    # we find a random node so we can atempt to connect to it
    ran = random.randint(0,len(nodes)-1)
    # we define the adress of the node by combining the ip address and the port
    addre = (nodes[ran],18000)
    # we duplicate the list of nodes so we can edit it later
    fake_list = nodes
    # we try to connect to the node
    try:
        client_socket.settimeout(1.0)
        client_socket.connect(addre)
        return nodes[ran]
    # if the node is not avalible we remove it from the list of nodes
    except:
        fake_list.remove(nodes[ran])
        # we iterate through the list and see if any of the nodes are avalible
        for i in range(len(fake_list)-1):
            if len(fake_list) == 0:
                # if there are no nodes avalible we display a message on the screen.
                print("no nodes currently avalible")
                return "no nodes currently avalible"
            ran = random.randint(0,len(fake_list)-1)
            # define the address
            addre = (fake_list[ran],18000)
            try:
                # try connect to the node
                client_socket.settimeout(1.0)
                client_socket.connect(addre)
                return fake_list[ran]
            except:
                # if the node is not responding we remove it from the list
                fake_list.remove(nodes[ran])

# try open the blockchain file and read it if it dosent exists we keep the new blockchain and set the balance to 10
try:
    fr = open("nat.blockchain",'r')
    blockc = fr.read()
    blockchain.chain = json.loads(blockc)
    fr.close()
    balance = get_from_blockchain('balance','most_rec')
except:
    # set the balance if there is no blockchain
    balance = float(10)

# to display an incoming transaction we want a nice formated box; as the length of the contents varys the box dynamicaly ajusts
def rec_box(fr, a):
    # top line, bottom line and center line
    top = ""
    center = "- You Recived " + a + " NAT From " + fr + " -"
    bt = ""
    # calculate the length of the center line ad check if it is even
    length = len(center)
    if((length % 2) == 0):
        # caluclate where to place 'RECV'
        half = length - 4
        half = half / 2
    else:
        # if the number is odd we make it even
        half = (length - 3) / 2
    # we make the top and bottom lines and add RECV
    for i in range(length - 3):
        if(i == half):
            top += "RECV"
            i += 4
        else:
            top += "-"
    for i in range(length):
        bt += "-"
    # return the box and contents
    return (top + "\n" + center + "\n" + bt)

# same as the rec_box function but this one has diffrent contents in the box
def snd_box(fr, a):
    top = ""
    center = "- You Sent " + fr + " NAT To " + a + " -"
    bt = ""
    length = len(center)
    if((length % 2) == 0):
        half = length - 4
        half = half / 2
    else:
        half = (length - 3) / 2
    for i in range(length - 3):
        if(i == half):
            top += "SEND"
            i += 4
        else:
            top += "-"
    for i in range(length):
        bt += "-"
    
    return (top + "\n" + center + "\n" + bt)

# the wallet has been succesfully launched
print("""
--------------------------------
-       NAT COIN WALLET        -
-         INITIALIZED          -
--------------------------------
\n""")

# read and load our config file    
config = configparser.ConfigParser()
config.read('dts.json')

# load the config file
passwd = config['details']['password']
id = config['details']['id']
cert = config['details']['cert']

# ask the user to enter their password
while True:
    passinput = getpass.getpass()
    # hash the password and see if the password is the same as the one in the file
    hash = hashlib.sha256()
    hash.update(passinput.encode())
    passinput = str(hash.digest())
    if passinput == passwd:
        # if the passwords match let the user in
        break

# wallet has been unlocked!
print("""
--------------------------------
-       NAT COIN WALLET        -
-          UNLOCKED            -
--------------------------------
\n""")

# give the user the options

print("""
             INFO:
            id : """+id+"""
wallet balance : """+str(balance)+"""

            COMMANDS:
          Send : Will initiate send module
  Transactions : Will show recent transactions
          Exit : Will exit the wallet
       Iptables: Will show ipadresses and thei usernames
     Blockchain: Will print the blockchain
\n\n""")

# this sends a request to the ip adress specified with the details specifed
def req(send_addr,rec_addr,amount,what,rec_name):
    # specifiy the data
    data = [send_addr,rec_name,amount]
    # convert it to a string
    data = str(data)
    # encode the data
    data = data.encode()
    # send the data
    client_socket.sendto(data,(str(rec_addr),9000))

# our function that send and recives the ip tables
def ip_tables():
    global addr,res_addr
    # find a node
    ip_addr = findNode()
    while True:
        # set the message and the ip & port
        message = str([get_ip_address(),id,'iptables'])
        message = message.encode()
        addre = (str(ip_addr), 18000)
        res_addr = addr
        # send the ip tables
        server_socket.sendto(message, addre)
        # try to recive data else we find an another node
        try:
            data, server = server_socket.recvfrom(1024)
            pre_addr = data.decode()
            addr = json.loads(pre_addr)
        except:
            ip_addr = findNode()
        
# this function runs in the backg =round to check for incoming transactions
def background():
    global balance
    # set the timeout
    server_socket.settimeout(5.1)
    while(True):
        # try to recive data if there is no data we just start again
            try:
                # recive data
                data, addrs = server_socket.recvfrom(9000)
                # process the data to make it into a list
                x = data.decode()
                x = x.strip("[]")
                x = x.replace("'","")
                x = x.replace(" ","")
                dt = x.split(',')
                # try to save it to the  blockchain and print the rec_box
                try:
                    # set the new balance
                    balance += float(dt[2])
                    # save to the blockchain
                    blockchain.save(dt[0],dt[1],dt[2],balance)
                    # print the box
                    print(rec_box(dt[2], dt[0]))
                except Exception as err:
                    pass
            except:
                pass

# the function we see
def foreground():
    global balance, config, id,res_addr, addr
    while True:
        # ask for an input
        do = input("\n$ ").lower()
        # check the users intentions
        if do == "send":
            # ask for the sender details
            to = input("Destination Username: ")
            if to != id:
                while(True):
                    # ask for the amount and check if it is a number
                    amm = input("Amount (NAT):")
                    try:
                        float(amm)
                        break
                    except:
                        print("The Amount You Entered Was Not A Number\n")
                # ask for a confermation
                conf = input("Are you sure? THIS CAN NOT BE UNDONE! y/n: ")
                if conf == "y":
                    # see if the user has enough funds
                    if (float(balance) == 0 or float(balance) - float(amm)) < 0:
                        print("TRANSACTION ERROR: INSUFFICENT FUNDS")
                    else:
                            try:               
                                    # set the balance and the amount to floating point numbers
                                    balance = float(balance)
                                    amm = float(amm)
                                    print("\n")
                                    # see if the destination online
                                    for i in range(4):
                                            print("Pinging Destination [" + str(i + 1) + " / 4]")
                                            echo_address = (str(addr[to]),9000)
                                            echo_socket.connect((echo_address))
                                            echo_socket.send("HEY?".encode())
                                            sleep(0.5)
                                    print("Ping Succsess\n")     
                                    # send a request     
                                    req(id,addr[to],amm,'amount',to)
                                    stramm = amm
                                    # print the transaction
                                    print(snd_box(str(stramm), str(to)))
                                    # subtract from the balance
                                    balance -= amm
                                    # save to the blockchain
                                    blockchain.save(id,to,amm,balance)
                            except ConnectionRefusedError:
                                # tell the user the destination is offline
                                print("TRANSACTION ERROR: DESTINATION IS OFFLINE")        

                else:
                    print("ABORTED\n")
            else:
                print("You can not send money to your self!")
        elif do == "transactions":
            transactions = ""
            # print the last 10 transactions made
            for i in range(10):
                    # get transactions from the blockchain
                    sender = get_from_blockchain('sender',i)
                    rec = get_from_blockchain('recipient',i)
                    amm = get_from_blockchain('amount',i)
                    amm = str(amm)
                    # see if the transaction is empty
                    if rec == "blank" or sender == "blank" or amm  == "blank":
                        pass
                    else:
                        transactions += ("to: " + rec + " from: " + sender + " amount: " + amm + "\n")
            if transactions == "":
                print("No recorded transactions")
            else:
                print(transactions)
        elif do == "exit":
            # exit
            exit()
        # this allows you to print the iptables
        elif do == "iptables":
             print("\n\n"+str(addr)+"\n\n")
        # you can print the blockchain!
        elif do == "blockchain":
                print(blockchain.chain)
        else:
                # tell the user if they entered an invlaid input
                print("could not read your query please try again.")

# define the threads
b = threading.Thread(name='background', target=background)
g = threading.Thread(name='ip_tables', target=ip_tables)
f = threading.Thread(name='foreground', target=foreground)

# start the threads
b.start()
f.start()
g.start()