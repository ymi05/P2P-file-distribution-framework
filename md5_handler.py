import hashlib

def convert_to_md5(filename):
	return hashlib.md5(open(filename,'rb').read()).hexdigest() 


def compare_md5(md5_merge,manifest_md5):
	return md5_merge == manifest_md5

 
