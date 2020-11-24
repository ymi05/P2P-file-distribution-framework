from md5_handler import convert_to_md5
import json , os


class ManifestFile:
    def __init__(self , fileName):
        self.data = {"numChunks" : 0 , "md5Checksum" : "" , "ports" : {}} #default structure for the manifest file
        self.fileName = fileName
        self.dir = "Manifests"
        if not os.path.exists(self.dir):
            os.makedirs(f"./{self.dir}") 

    def prepareManifestFile(self , numberOfChunkHolders):
        self.data["numChunks"] = numberOfChunkHolders
        self.data["md5Checksum"]= convert_to_md5(f"Server_files/{self.fileName}")

    def addChunkDetails(self , chunkID , IP_Address , portNo):
        self.fileName = self.fileName.split("/")[-1]
        newData = {
            'name': self.fileName.split(".")[0]+"_chunk"+str(chunkID)+"."+self.fileName.split(".")[1],
            'id':chunkID,
            'IP_Address': "127.0.0.1",
            'port': int(portNo)
        }
                
        if portNo not in self.data["ports"]:
            self.data["ports"][portNo] = ({
                'chunks':[newData]
                        
            })
        else:
            self.data["ports"][portNo]['chunks'].append(newData)
            


    def saveAsFile(self):   
        
        fileName = self.fileName.split(".")[0]
        with open(f"{self.dir}/{fileName}_manifest.json",'w') as manifest:
		        manifest.write(json.dumps(self.data,  indent=4))
    
    def getMd5(self):
        return self.data["md5Checksum"]
       