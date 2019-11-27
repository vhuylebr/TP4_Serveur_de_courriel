# 111 274 586 HUYLEBROECK Valerian
# 111 276 568 LAABID Zackaria
import sys
import optparse
import socket
import random
from cryptoModule import entierAleatoire, trouverNombrePremier, exponentiationModulaire
from socketUtil import send_msg, recv_msg
from datetime import datetime


def isIpAddress(option, opt_str, ipAddress, parser):
    socket.inet_aton(ipAddress)
    setattr(parser.values, option.dest, ipAddress)


try:
    parser = optparse.OptionParser()

    parser.add_option("-p", "--port", action="store", dest="port", type="int")
    parser.add_option("-s", "--serveur", action="store_true",
                      dest="isServer", default=False)
    parser.add_option("-d", "--destination",
                      action="callback", dest="destination", type="string", callback=isIpAddress, default="localhost")
    opts = parser.parse_args(sys.argv[1:])[0]

    if opts.isServer and opts.destination != "localhost":
        raise Exception(
            "L'application ne peut pas utiliser -d et -s simultanément")
    if not opts.port:
        raise Exception("L'option -p est obligatoire")

    print("###############################################################")
    if opts.isServer:
        print("Demarrage du serveur ...")
        a = trouverNombrePremier()
        b = entierAleatoire(a)
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serversocket.bind(("localhost", opts.port))
        serversocket.listen(5)
        print("Ecoute sur le port :", opts.port)
        (s, address) = serversocket.accept()
        print("1e connexion au serveur\n----------------------------------------------------------")
        send_msg(s, str(a))
        print("Envoi du modulo :", a)
        send_msg(s, str(b))
        print("Envoi de la base :", b,
              "\n----------------------------------------------------------")
        q = entierAleatoire(int(a))
        print("Cle privee :", q)
        A = exponentiationModulaire(b, q, a)
        send_msg(s, str(A))
        print("Cle publique a envoyer :", A)
        B = recv_msg(s)
        print("Cle publique recue : ", B)
        k = exponentiationModulaire(int(B), q, a)
        print("Cle partagee :", k)
        s.close()
        print("au serveur")
    else:
        destination = (opts.destination, opts.port)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(destination)
        a = recv_msg(s)
        print("Reception du modulo :", a)
        b = recv_msg(s)
        print("Reception de la base :", b,
              "\n----------------------------------------------------------")
        p = entierAleatoire(int(a))
        print("Cle privee :", p)

        B = exponentiationModulaire(int(b), p, int(a))
        send_msg(s, str(B))
        print("Cle publique a envoyer :", B)
        A = recv_msg(s)
        print("Cle publique recue : ", A)
        k = exponentiationModulaire(int(A), p, int(a))
        print("Cle partagee :", k)
        s.close()

    print("###############################################################")
except Exception as err:
    file = open("Error.log", "a")
    file.write(str(datetime.now()) + ": " + str(err) + "\n")
    file.close()
    print(err)
