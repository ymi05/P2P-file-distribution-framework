import json 



numberOfChunks = 0
md5Checksum = ""


with open(f'Manifests/HW6.' ,) as manifestFile:
    
  fileData = json.load(manifestFile)

numberOfChunks = fileData["numChunks"]
md5Checksum = fileData["md5Checksum"]

chosenFiles = []
for chunk in fileData["chunks"]:
    values = chunk.values()
    value_iterator = iter(values)
    values = next(value_iterator)
    

    if (fileName:= values["name"]) not in chosenFiles: #since the manifest contains info for copies of the same chunk, we want to avoid unecessary requests
        chosenFiles.append(fileName)
        IP_Address = values["IP_Address"]
        port = int(values["port"])
        requestChunks(fileName , port)
        