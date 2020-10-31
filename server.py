import socket
import threading
import os


def retriveFile(name, sock):
    fileName = sock.recv(1024)
    if os.path.isfile(fileName):
        sock.send(f"EXISTS {os.path.getsize(fileName)}".encode())
        userResponse = sock.recv(1024).decode()
        if userResponse[:2] == "OK":
            with open(fileName, 'rb') as f:
                bytesToSend = f.read(1024)
                sock.send(bytesToSend)
                while bytesToSend != "":
                    bytesToSend = f.read(1024)
                    sock.send(bytesToSend)

    else:
        sock.send("ERR".encode())

    sock.close()


def Main():
    host = "127.0.0.1"
    port = 5000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(5)

    print("Server started.")
    while True:
        c, addr = s.accept()
        print(f"Client connected IP < {addr} >")
        t = threading.Thread(target=retriveFile, args=("retriveThread", c))
        t.start()
    s.close()


if __name__ == "__main__":
    Main()
