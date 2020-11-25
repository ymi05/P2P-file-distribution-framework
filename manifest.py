from md5_handler import convert_to_md5
import json , os


class ManifestFile:
    def __init__(self , fileName = None):
        self.dir = "Manifests"
        if not os.path.exists(self.dir):
            os.makedirs(f"./{self.dir}") 
        if fileName != None:
            self.data = {"numChunks" : 0 , "md5Checksum" : "" , "ports" : {}} #default structure for the manifest file
            self.fileName = fileName

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
  
    @staticmethod
    def reconstructManifest(portNoOfChurnedPeer , * , manifestFile , sendFileToNewPeer ):
        fileData = None
        send_File_From_To = {}
        file_dest_array = []
        newData = None
        dataToBeAdded = {}
        with open(f'Manifests/{manifestFile}' ,) as currentManifestFile:
                
            fileData = json.load(currentManifestFile)

            portNumbers = fileData["ports"]
            try:
                portNoChunks = portNumbers[str(portNoOfChurnedPeer)]["chunks"]
            except:
                return -1
            fileName_Source = {}
            fileName_Destination = {}
 

            for chunkInfo in portNoChunks:
                fileName_Source[chunkInfo["name"]] = 0
                fileName_Destination[chunkInfo["name"]] = 0

            
            for portNo in portNumbers:
                if int(portNo) != int(portNoOfChurnedPeer):
                    portNoChunks = portNumbers[portNo]["chunks"]

                    filesAtCurrentPeer = []
                    for fileName in fileName_Source:
                        hasFile = False
                        for chunkInfo in portNoChunks:
                            if fileName == chunkInfo['name']:
                                hasFile = True
                                fileName_Source[fileName] = int(portNo)
                                dataToBeAdded[int(portNo)] = []


                        if not hasFile:
                            fileName_Destination[fileName] = int(portNo)

        currentManifestFile.close()
                    
                        
                         
       
        for fileName in fileName_Source:
            # sendFileToNewPeer(sourcePortNo = fileName_Source[fileName] , destinationPortNo = fileName_Destination[fileName] , chunkFileName = fileName)
            portNumber = fileName_Destination[fileName]
            try:
                dataToBeAdded[fileName_Destination[fileName]].append({
                        'name': fileName,
                        'id': -1,
                        'IP_Address': "127.0.0.1",
                        'port': fileName_Destination[fileName]
                })
             

            except:
                pass
            
          

        del fileData["ports"][str(portNoOfChurnedPeer)]

        for port in dataToBeAdded:
            fileData["ports"][str(port)]["chunks"].extend(dataToBeAdded[port])

        updatedManifestFile = open(f'./Manifests/{manifestFile}' , 'w')

        
        updatedManifestFile.write(json.dumps(fileData , indent=4))
        updatedManifestFile.close()

    
    
    def getMd5(self):
        return self.data["md5Checksum"]
       