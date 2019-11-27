import socket
import getpass
from socketUtil import send_msg, recv_msg
import re
regex = re.compile(
    "^(?=.*[a-z])(?=.*[A-Z])(?=(.*\d){2})[a-zA-Z\d]{6,12}$")
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    destination = ("127.0.0.1", 1234)
    s.connect(destination)
except:
    print("Problème de connection au serveur.")
    exit()

print("Menu de connexion")
print("1. Creer un compte")
print("2. Se connecter")
while True:
    try:
        n = int(input())
        if n < 1 or n > 2:
            print("Taper 1 pour créer un compte or 2 pour vous connecter.")
        else:
            break
    except ValueError:
        print("Taper 1 pour créer un compte or 2 pour vous connecter.")
isValid = False
while isValid != True:
    name = input("username:")
    password = getpass.getpass("Password : ")
    send_msg(s, str(n))
    send_msg(s, name)
    send_msg(s, password)
    isValid = recv_msg(s) == "True"
    if (isValid == False):
        print(recv_msg(s))
while True:
    print("Menu principal")
    print("1. Consultation de courriels")
    print("2. Envoi de courriels")
    print("3. Statistiques")
    print("4. Quitter")
    try:
        n = int(input())
        if n < 1 or n > 4:
            continue
        else:
            if n == 2:
                dest = input("l'adresse de destination:")
                sujet = input("sujet:")
                corps = input("le corps du message:")
            if n == 4:
                exit()
    except ValueError:
        continue
