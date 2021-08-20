#---------------------------------#
#-        NAT-Coin v1.0.0        -#
#-   Copyright Dima Galkin 2021  -#
#---------------------------------#

try:
    import json
except:
    print("Json Is Not Instaled Please Install It.")
    input("Press any key to exit.")
    exit()

nodejn = open("nodes//node.json","w")
nodejw = open("NAT//node.json","w")

contents = ("""
[verif]
""")
verif = []

for i in range(4):
    ip = input("Enter node ip " + str(i + 1) + " (if non enter 0): ")
    contents += ("\nip" + str(i+1) + " = " + ip)
    verif.append(ip)

nodejn.write(contents)
verif = json.dumps(verif)
nodejw.write(verif)

nodejn.close()
nodejw.close()