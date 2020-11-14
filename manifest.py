from md5_handler import convert_to_md5
import json , os


class ManifestFile:
    def __init__(self , fileName):
        self.data = {"numChunks" : 0 , "md5Checksum" : "" , "chunks" : []} #default structure for the manifest file
        self.fileName = fileName

    def prepareManifestFile(self , numberOfChunkHolders):
        self.data["numChunks"] = numberOfChunkHolders
        self.data["md5Checksum"]= convert_to_md5(self.fileName)

    def addChunkDetails(self , chunkID , IP_Address , portNo):
        self.fileName = self.fileName.split("/")[-1]
        self.data["chunks"].append({
                    'name': self.fileName.split(".")[0]+"_chunk"+str(chunkID)+"."+self.fileName.split(".")[1],
                    'id':chunkID,
                    'IP_Address': "127.0.0.1",
                    'port': int(portNo)
                })

    def saveAsFile(self):
        dir = "Manifests"
        if not os.path.exists(dir):
            os.makedirs(f"./{dir}")    
        
        with open(f"{dir}/{self.fileName}_manifest.json",'w') as manifest:
		        manifest.write(json.dumps(self.data,  indent=4))
       