#---------------------------------#
#-        NAT-Coin v1.0.0        -#
#-   Copyright Dima Galkin 2021  -#
#---------------------------------#


# Below the program checks that all the requiered modules are installed and if not the user is requestes to install it

try:
    import random
except:
    print("Random Is Not Instaled Please Install It.")
    input("Press any key to exit.")
    exit()

try:
    import string
except:
    print("String Is Not Instaled Please Install It.")
    input("Press any key to exit.")
    exit()

try:
    import datetime
except:
    print("Datetime Is Not Instaled Please Install It.")
    input("Press any key to exit.")
    exit()

try:
    import hashlib
except:
    print("Hashlib Is Not Instaled Please Install It.")
    input("Press any key to exit.")
    exit()

# this generates a unique user id
def get_random_id(gg):
    random_source = string.ascii_letters + string.digits + string.punctuation
    password = random.choice(string.ascii_lowercase)
    password += random.choice(string.ascii_uppercase)
    password += random.choice(string.digits)
    for i in range(gg):
        password += random.choice(random_source)
    password_list = list(password)
    random.SystemRandom().shuffle(password_list)
    password = ''.join(password_list)
    # based on the time to the milisecond so duplicate ids are impossible
    date = str(datetime.datetime.now())
    date += password
    date += "=="
    date = date.replace("-","")
    date = date.replace(" ","")
    date = date.replace(":","")
    date = date.translate ({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"})
    return date

# generate the random id
id = get_random_id(10)

# set the password
while True:
	password = input("Set your password: ")
	repass = input("retype your password: ")
	if password == repass:
		break
	print("try again")
	
# hash the password
hash = hashlib.sha256()
hash.update(password.encode())
passwd = str(hash.digest())

# create and set the file
cert = get_random_id(100)
file = open("dts.json","w")
file.write("""
[details]
id = """ + id + """

password = """ + passwd + """

cert = """+cert+"""
""")
file.close()
print("done")
