import socket
import base64
import threading
import time
import random
import string
import datetime
import getpass
import configparser
from subprocess import call
import os
import json
from time import sleep
import hashlib
import json
from time import time

nodes = ['192.168.0.15','192.168.0.20']
global res_addr, addr

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.new_block(previous_hash="The times date",proof=100)

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.pending_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.pending_transactions = []
        self.chain.append(block)

        return block

    @property
    def last_block(self):

        return self.chain[-1]

    def num_block(self,num):
        num = 0 - num
        return self.chain[num]

    def new_transaction(self, sender, recipient, amount,balance):
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
            'balance' : balance
        }
        self.pending_transactions.append(transaction)
        return self.last_block['index'] + 1

    def hash(self,block):
        string_object = json.dumps(block, sort_keys=True)
        block_string = string_object.encode()

        raw_hash = hashlib.sha256(block_string)
        hex_hash = raw_hash.hexdigest()

        return hex_hash

    def save(self,to,fro,amm,balance):
        t1 = blockchain.new_transaction(to,fro,amm,balance)
        blockchain.new_block(12345)
        f = open("nat.blockchain",'w')
        f.write(json.dumps(blockchain.chain))
        f.close()
        

blockchain = Blockchain()

def get_from_blockchain(what,num):
    if num == 'most_rec':
        num = len(blockchain.chain) - 1
    else:
        num = 0 - num
    try:
        action = blockchain.chain[num]
        transaction = action['transactions']
        transaction = transaction[0]
        return transaction[what]
    except:
        return 'blank'


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('', 9000))

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(1.0)

fee = float(0.05)

def findNode():
    ran = random.randint(0,len(nodes)-1)
    addr = (nodes[ran],18000)
    fake_list = nodes
    try:
        client_socket.settimeout(1.0)
        client_socket.connect(addr)
        return nodes[ran]
    except:
        fake_list.remove(nodes[ran])
        for i in range(len(fake_list)-1):
            print("i")
            if len(fake_list) == 0:
                return "no nodes currently avalible"
            ran = random.randint(0,len(fake_list)-1)
            addr = (fake_list[ran],18000)
            try:
                client_socket.settimeout(1.0)
                client_socket.connect(addr)
                return fake_list[ran]
            except:
                fake_list.remove(nodes[ran])

try:
    fr = open("nat.blockchain",'r')
    blockc = fr.read()
    blockchain.chain = json.loads(blockc)
    fr.close()
    balance = get_from_blockchain('balance','most_rec')
except:
    balance = float(10)

print("""
--------------------------------
-       NAT COIN WALLET        -
-         INSTALIZED           -
--------------------------------
\n""")

def clear():
    _ = call('clear' if os.name =='posix' else 'cls')
    
config = configparser.ConfigParser()
config.read('dts.json')

passwd = config['details']['password']
id = config['details']['id']
cert = config['details']['cert']

while True:
    passinput = getpass.getpass()
    if passinput == passwd:
        break
    print('incorrect password: try again')

print("""
--------------------------------
-       NAT COIN WALLET        -
-          UNLOCKED            -
--------------------------------
\n""")

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

addres = {}

def req(send_addr,rec_addr,amount,what,rec_name):
    data = ""
    local_ip = get_ip_address()
    data = [send_addr,rec_name,amount]
    data = str(data)
    data = data.encode()
    client_socket.sendto(data,(str(rec_addr),9000))

def ip_tables():
    global addr,res_addr
    ip_addr = findNode()
    while True:
        message = str([get_ip_address(),id,'iptables'])
        message = message.encode()
        addr = (str(ip_addr), 18000)
        res_addr = addr
        client_socket.sendto(message, addr)
        try:
            data, server = client_socket.recvfrom(1024)
            pre_addr = data.decode()
            addr = json.loads(pre_addr)
        except:
            ip_addr = findNode()
        sleep(1)

def background():
    global balance
    server_socket.settimeout(5.1)
    while(True):
            try:
                data, addrs = server_socket.recvfrom(9000)
                x = data.decode()
                x = x.strip("[]")
                x = x.replace("'","")
                x = x.replace(" ","")
                dt = x.split(',')
                try:
                    balance += float(dt[2])
                    blockchain.save(dt[0],dt[1],dt[2],balance)
                    print("""
                    -------------------RECIVE---------------------------------------
                    -   You Recived """ + dt[2] + """ NAT From """ + dt[0] + """ -
                    ----------------------------------------------------------------
                    """)
                except Exception as err:
                    print("OS error: {0}".format(err))
                    print("pass")
            except:
                pass

def foreground():
    global balance, fee, config, id,res_addr
    while True:
        do = input("\n$ ").lower()
        if do == "send":
            to = input("Destination Username: ")
            if to != id:
                amm = input("Amount (NAT):")
                conf = input("Are you sure? THIS CAN NOT BE UNDONE! y/n: ")
                if conf == "y":
                    if (float(balance) == 0 or float(balance) - float(amm)) < 0:
                        print("TRANSACTION ERROR: INSUFFICENT FUNDS")
                    else:
                        try:
                                    balance = float(balance)
                                    amm = float(amm)
                                    oramm = amm
                                    mfee = amm * fee
                                    amm = float(amm - mfee)
                                    balance = balance - oramm
                                    req(id,addr[to],amm,'amount',to)
                                    blockchain.save(id,to,amm,balance)
                                    print("""
                                    ------------------SEND---------------------------------------------
                                    -   You Sent """ + str(amm) + """ NAT To """ + to + """ -
                                    -------------------------------------------------------------------
                                    """)
                                    
                        except KeyError:
                                    print("TRANSACTION ERROR: DESTENATION DOES NOT EXIST")

                else:
                    print("ABORTED\n")
            else:
                print("You can not send money to your self!")
        elif do == "transactions":
            transactions = ""
            for i in range(10):
                    sender = get_from_blockchain('sender',i)
                    rec = get_from_blockchain('recipient',i)
                    amm = get_from_blockchain('amount',i)
                    amm = str(amm)
                    if rec == "blank" or sender == "blank" or amm  == "blank":
                        pass
                    else:
                        transactions += ("to: " + rec + " from: " + sender + " amount: " + amm + "\n")
            if transactions == "":
                print("No recorded transactions")
            else:
                print(transactions)
        elif do == "exit":
                exit()
        elif do == "iptables":
             print("\n\n"+str(addr)+"\n\n")
        elif do == "blockchain":
                #print(get_from_blockchain('sender','most_rec'))
                print(blockchain.chain)
        else:
                print("could not read your query please try again.")
    
b = threading.Thread(name='background', target=background)
g = threading.Thread(name='ip_tables', target=ip_tables)
f = threading.Thread(name='foreground', target=foreground)

b.start()
f.start()
g.start()

#v = ui.load_view()
#v.present('sheet')
