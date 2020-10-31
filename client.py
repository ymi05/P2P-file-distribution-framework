import socket


def Main():
    host = "127.0.0.1"
    port = 5000

    s = socket.socket(socket.AF_INE, socket.SOCK_STREAM)
    s.connect((host, port))

    filename = input("Filename? -->")
    if filename != "q":
        s.send(filename.encode())
        data = s.recv(1024).decode()
        if data[:6] == "EXISTS":
            filesize = (int(data[6:]))
            message = input(f"File Exists , {filesize} Bytes. Download?(Y/N)")
            if message == "Y":
                s.send("OK".encode())
                f = open(f"Client_downloads/new_{filename}", "wb")
                data = s.recv(1024)

                totalReceived = len(data)
                f.write(data)
                while totalReceived < filesize:
                    data = s.recv(1024)

                    totalReceived += len(data)
                    f.write(data)
                    print("{0:.2f").format(
                        (totalReceived / float(filesize) * 100) + "%Done")
                f.close()
                print("Download Complete")
        else:
            print("File does not exist!")

    s.close()


if __name__ == "__main__":
    Main()
