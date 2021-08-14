# NAT-Coin
This is a crypto currency made in python.

# How
- the program uses sockets to comunicate with other peers and nodes on your network.
- it utilizes blockchain technology to record all transactions made by the user and also their wallet balance.
- you have a unique randomly generated user id which is mapped to your ip addres when you connect to a node
- the username is generated by geting the current date and time to the second so duplicate user id's are highly unlikley.
- The wallet is per person, when you first launch it it asks for you to set a password.
- The wallet can check for connected nodes and switch nodes on the fly if requiered.
- There are anywere from 1 to 4 nodes running at the same time.

# Nodes
- The nodes are listning for any incoming requests frim clients
- When a node recives a request it adds the clients user name and ip to a dict and sends the dict of all the users and
their ip's back to the user
- The nodes connect to eachother and send the usrenames and corresponding ip's to eachother to compare and adapt their [iptables](#iptables).

# Iptables
These are tables are a dictionary that contains the username of the user and their ip address because the wallet uses user id's but the wallet needs the ip address of the destination. The users wallet checks the iptable that it was sent by the node and it returns the ip address of the specified users uid so then the wallet can send the request.

# Get Nodes
This function finds avalible nodes based on a list of verified node ip addresses. How? The function generates a random number from 0 to `len(addresses) - 1`, and trys to connect to the ip address in that position in the list `addr = addresses[randomNumber]` and then try to initiate a connection with that ip address using `socket.connect(addr)`. If this works we use this address as our node otherwise we copy our list of ip addresses `back_ips = addresses` and we remove the ip address which just failed `back_ips.remove(addr)` and then repeat the prosses until we tried all the ip adresses.

# Blockchain
We create a class called `Blockchain` and then we create many diffrent functions like `new_block()` and `new_transaction()`. When a new block is created the function gets all recent transactions and add them to a dictionary (the block) which is later appended to a list (the chain). When a user makes a transactions it gets added to their recent transactions or if they recive a transaction it gets loaded to the blockchain. Once the blockchain has been modified it is imedietly saved to a file (.blockchain).

# Requierments
socket, base64, threading, time, random, string, datetime, getpass, configparser, subprocess, os, hashlib, json, python

# Installation

> Note that only one wallet can be running on a machine at one time and only one node can be running on a machine at one time but as they use diffrent ports you can run one node and one wallet on the same machine at the same time. 

### Using the installer
1. download the installer from the latest release
2. launch it
3. once finished you can find the node and wallet apps in your app list
4. launch the wallet and go through the first time setup

### Manualy
1. download the latest release
2. extract the files
4. launch the wallet and go through the first time setup
 
# Instructions

### How to use a node
It is actualy pretty simple, all you have to do is double click on the `node.py` file and your done unless you used the installer, then you just have to launch it via the app menu, if everythig is working then it should just show a black screen. If there is an error then just raise an issue.

### How to use the Wallet
Launch the wallet like the node and enter the password you set during the first time setup, then it will present you some options chose one and then follow the instructions. If there is an error on screen then raise an issue