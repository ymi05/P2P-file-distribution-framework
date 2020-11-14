import json as json
import hashlib


def convertmd5(filename):
	return  hashlib.md5(open(filename,'rb').read()).hexdigest()

data={"numChunks" : 0 , "md5Checksum" : "" , "chunks" : []}
volunteers=[('17.0.12',5000),('17.0.16',5001),('17.0.34',5004)]

def prepareManifestfile(filename):
	data["numChunks"]=len(volunteers)
	data["md5Checksum"]=convertmd5(filename)
	data["chunks"]=[]
	
	for x in volunteers:
		data["chunks"].append({
			'name':filename.split(".")[0]+"_chunk"+str(volunteers.index(x))+"."+filename.split(".")[1],
			'id':volunteers.index(x),
			'ip':x[0],
			'port':x[1]
		})
	
	with open('Manifest_'+filename+'.json','w') as manifest:
		manifest.write(json.dumps(data, indent=4))
	manifest.close()


prepareManifestfile("md5.py")
