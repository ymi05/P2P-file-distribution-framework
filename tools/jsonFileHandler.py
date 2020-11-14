import json

def getDataAndRequestChunks(manifestFileName , func):
    numberOfChunks = 0
    md5Checksum = ""
    with open(manifestFileName ,) as manifestFile:
        fileData = json.load(manifestFile)

        numberOfChunks = fileData["numChunks"]
        md5Checksum = fileData["md5Checksum"]
        print(md5Checksum)
        for chunk in fileData["chunks"]:
            IP_Address = chunk["IP_Address"]
            port = chunk["port"]
            func(IP_Address , port)


    

    
