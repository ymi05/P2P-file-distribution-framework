import os
fileList = os.listdir(f'./Peers/Pia/Downloads')
print(fileList)
print((f"{'sample.txt'.split('.')[0]}_chunk_"))
fileList = list(filter(lambda file: file.startswith(f"{'sample.txt'.split('.')[0]}_"), fileList))
# fileList.sort(key = len)
print(fileList)




