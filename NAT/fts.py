import random
import string
import datetime

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
    date = str(datetime.datetime.now())
    date += password
    date += "=="
    date = date.replace("-","")
    date = date.replace(" ","")
    date = date.replace(":","")
    date = date.replace("!@#$%^&*()[]{};:,./<>?\|`~-_+", " ")
    return date
id = get_random_id(10)

while True:
	password = input("Set your password: ")
	repass = input("retype your password: ")
	if password == repass:
		break
	print("try again")
	
cert = get_random_id(100)
file = open("dts.json","w")
file.write("""
[details]
id = """ + id + """

password = """ + password + """

cert = """+cert+"""

balance = 0
""")
file.close()
print("done")
