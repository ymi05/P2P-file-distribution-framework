import json

def getDataAndRequestChunks(peerName , manifestFileName , requestChunks):
    numberOfChunks = 0
    md5Checksum = ""


    with open(f'Peers/{peerName}/Downloads/{manifestFileName}' ,) as manifestFile:
        
      fileData = json.load(manifestFile)

      numberOfChunks = fileData["numChunks"]
      md5Checksum = fileData["md5Checksum"]

      chosenFiles = []
      ports = fileData["ports"]
      for portNo in ports:
        for chunk in ports[portNo]["chunks"]:
        
          if (fileName:= chunk["name"]) not in chosenFiles: #since the manifest contains info for copies of the same chunk, we want to avoid unecessary requests
              chosenFiles.append(fileName)
              IP_Address = chunk["IP_Address"]
              port = int(chunk["port"])
              requestChunks(fileName , port)
              
            
      return md5Checksum
      


    

    
