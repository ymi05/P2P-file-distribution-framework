# import json 



# numberOfChunks = 0
# md5Checksum = ""

# fileData = None
# with open('Manifests/Project_manifest.json' ,) as manifestFile:
    
#   fileData = json.load(manifestFile)

#   portNumbers = fileData["ports"]
#   portNoChunks = portNumbers["5005"]["chunks"]
#   filesToBeSent = []
#   for chunkInfo in portNoChunks:
#     filesToBeSent.append(chunkInfo["name"])
#   print(filesToBeSent)

#   for portNo in portNumbers:
#     portNoChunks = portNumbers[portNo]["chunks"]
#     for chunkInfo in portNoChunks:
#       if (chosenFile:=chunkInfo["name"]) in filesToBeSent:
#         #send file to randomPeer
#         filesToBeSent.remove(chosenFile)

#   # print(filesToBeSent)

# with open('Manifests/Project_manifest.json' ,'w') as manifestFile:

#   del fileData["ports"]["5005"]
#   manifestFile.write(json.dumps(fileData , indent=4))

    

    

import os
fileList = os.listdir('./Manifests')
print(fileList)