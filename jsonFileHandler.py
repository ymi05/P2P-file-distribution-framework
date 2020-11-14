import json

def getDataAndRequestChunks(peerName , manifestFileName , requestChunks):
    numberOfChunks = 0
    md5Checksum = ""


    with open(f'Peers/{peerName}/Downloads/{manifestFileName}' ,) as manifestFile:
        
        fileData = json.load(manifestFile)

        numberOfChunks = fileData["numChunks"]
        md5Checksum = fileData["md5Checksum"]


        for chunk in fileData["chunks"]:
            IP_Address = chunk["IP_Address"]
            port = int(chunk["port"])
            fileName = chunk["name"]
            requestChunks(fileName , port)


    

    
