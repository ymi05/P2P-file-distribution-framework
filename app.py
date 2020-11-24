from peer import Peer


def Main():
    name = input("Enter your name please: ")
    newPeer = Peer(name, portNumber= 5030,allowConnection=True)

    newPeer.connect(justGetID= False)
    print("You are now connected to the server!")
    print(f"Hello {newPeer.name}! Your ID is {newPeer.id}")
    filename = input("Please enter the filename: ")
    newPeer.requestFile(filename)

    

if __name__ == "__main__":
    Main()
