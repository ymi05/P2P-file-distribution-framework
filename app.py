from peer import Peer


def Main():
    name = input("Enter your name please: ")
    newPeer = Peer(name, allowConnection=True)
    print(f"Hello {newPeer.name}! Your ID is {newPeer.id}")
    newPeer.connect()
    print("You are now connected to the server!")
    filename = input("Please enter the filename: ")
    newPeer.requestFile(filename)


if __name__ == "__main__":
    Main()
