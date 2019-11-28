import socket
from socketUtil import send_msg, recv_msg
import re
import os
from hashlib import sha256
from email.mime.text import MIMEText

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
    f.close()
while True:
    option = recv_msg(s)
    if option == "2":
        emailAddress = recv_msg(s)
        sujet = recv_msg(s)
        corps = recv_msg(s)

        # creation du courriel
        courriel = MIMEText(corps)
        courriel["From"] = name + "@glo2000.ca"
        courriel["To"] = emailAddress
        courriel["Subject"] = sujet
        if (emailAddress.find("@glo2000.ca") != -1):
            if os.path.isdir("./" + emailAddress[:-11]) == False:
                if os.path.isdir("./ERREUR") == False:
                    os.mkdir("ERREUR")
                f = open("./ERREUR/" + sujet, "a+")
                f.write("From: " + courriel["From"] + "\n")
                f.write("To: " + courriel["To"] + "\n")
                f.write("Sujet: " + courriel["Subject"] + "\n")
                f.write("Message: " + corps + "\n")
                f.close()
                send_msg(
                    s, "L’envoi n’a pas pu etre effectue destinataire inconnu.")
            else:
                path = "./" + emailAddress[:-11] + "/" + sujet
                f = open(path, "a+")
                f.write("From: " + courriel["From"] + "\n")
                f.write("To: " + courriel["To"] + "\n")
                f.write("Sujet: " + courriel["Subject"] + "\n")
                f.write("Message: " + corps + "\n")
                f.close()
                send_msg(s, "Le courriel a bien ete envoye! ")
        else:  # envoi du courriel
            try:
                smtpConnection = smtplib.SMTP(
                    host="smtp.ulaval.ca", timeout=10)
                smtpConnection.sendmail(
                    courriel["From"], courriel["To"], courriel.as_string())
                smtpConnection.quit()
                send_msg(s, "Le courriel a bien ete envoye! ")
            except:
                send_msg(s, "L’envoi n’a pas pu etre effectue.")
    if option == "4":
        s.close()
        break
    if option == "1":
        listOfSubject = os.listdir("./" + name)
        listOfSubject.remove("config.txt")
        if len(listOfSubject) == 0:
            send_msg(s, "")
        else:
            listOfSubjectText = ""
            for i in range(len(listOfSubject)):
                listOfSubjectText += str(i) + ". " + listOfSubject[i] + "\n"
            send_msg(s, listOfSubjectText)
            idSubject = int(recv_msg(s))
            subjectPath = "./" + name + "/" + listOfSubject[idSubject]
            f = open(subjectPath, "r")
            send_msg(s, f.read())
            f.close()
    if option == "3":
        subjects = os.listdir("./" + name)
        subjects.remove("config.txt")
        size = 0
        listMessageBySubject = ""
        for subject in subjects:
            size += os.path.getsize("./" + name + "/" + subject)
            f = open("./" + name + "/" + subject, "r")
            listMessageBySubject += subject + "\n"
            listMessageBySubject += f.read()
            f.close()
        send_msg(s, "vous avez " +
                 str(listMessageBySubject.count("To")) + " messages\n" + "la taille du dossier est de " + str(size) + " octets\n" + "Voici ci-dessous la liste  des messages par sujet:\n" + listMessageBySubject)
