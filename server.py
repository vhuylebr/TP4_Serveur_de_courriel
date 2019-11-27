import socket
from socketUtil import send_msg, recv_msg
import re
import os
from hashlib import sha256

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.bind(("localhost", 1234))
serverSocket.listen(5)
regex = re.compile(
    "^(?=.*[a-z])(?=.*[A-Z])(?=(.*\d){2})[a-zA-Z\d]{6,12}$")
print("Ecoute sur le port :", 1234)
(s, address) = serverSocket.accept()
isValid = False
while isValid != True:
    flag = recv_msg(s)
    name = recv_msg(s)
    password = recv_msg(s)
    if (flag == "2"):
        isValid = os.path.isdir("./" + name)
        if isValid == False:
            send_msg(s, "False")
            send_msg(s, "L'utilisateur n'existe pas.")
            continue
        f = open("./" + name + "/config.txt", "r+")
        hashedText = sha256(password.encode()).hexdigest()
        isValid = f.read() == hashedText
        if isValid == False:
            send_msg(s, "False")
            send_msg(s, "L'utilisateur n'existe pas.")
            continue
    elif (flag == "1"):
        isValid = bool(regex.match(password))
        if isValid == False:
            send_msg(s, "False")
            send_msg(s, "le mot de passe contient entre 6 et 12 caractères, dont au moins deux chiffres, une lettre majuscule, une lettre minuscule")
            continue
        isValid = os.path.isdir("./" + name) != True
        if isValid == False:
            send_msg(s, "False")
            send_msg(s, "L'utilisateur existe déja.")
            continue
    else:
        send_msg(s, "false")
    send_msg(s, "True")
if (flag == "1"):
    os.mkdir(name)
    f = open("./" + name + "/config.txt", "w+")
    hashedText = sha256(password.encode()).hexdigest()
    f.write(hashedText)
