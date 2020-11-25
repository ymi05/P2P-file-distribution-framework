import json 

numberOfChunks = 0
md5Checksum = ""

with open(f'Manifests/Project_manifest.json' ,) as manifestFile:

    fileData = json.load(manifestFile)

    numberOfChunks = fileData["numChunks"]
    md5Checksum = fileData["md5Checksum"]

    chosenFiles = []
    ports = fileData["ports"]
    for portNoDetails in ports:

        for chunk in ports[portNoDetails]["chunks"]:
        
            if (fileName:= chunk["name"]) not in chosenFiles: #since the manifest contains info for copies of the same chunk, we want to avoid unecessary requests
                chosenFiles.append(fileName)
                IP_Address = chunk["IP_Address"]
                port = int(chunk["port"])
                # requestChunks(fileName , port)
                print(port)
            
            
# return md5Checksum