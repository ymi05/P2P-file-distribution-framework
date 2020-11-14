from socket import *


newSocket = socket(AF_INET, SOCK_STREAM)
newSocket.bind(("" , 5434))
newSocket.connect_ex(("localhost", 5003))


newSocket.send("HEre".encode())