import os
import math

# # merge
# mylist = os.listdir('.')
# mylist = list(filter(lambda k: k.startswith('ex_json_part'), mylist))
# mylist.sort(key=lambda x: int(x[len('ex_json_part'):]))
# print(mylist)

# for file in mylist:
#     with open('full_file', 'ab') as total_file:
#         with open(file, 'rb') as chunk_file:
#             for line in chunk_file:
#                 total_file.write(line)

# merge
def mergeFiles(requestFileName):

    fileList = os.listdir('./DividedFiles/')
    fileList = list(filter(lambda file: file.startswith(f"{requestFileName.split('.')[0]}_chunk_"), fileList))
    fileList.sort(key = len)
    print(fileList)

    for file in fileList:
        with open(requestFileName, 'ab') as total_file:
            with open(f"DividedFiles/{file}", 'rb') as chunk_file:
                for line in chunk_file:
                    total_file.write(line)

mergeFiles("app.txt")
# divide into chunks
# CHUNK_SIZE = int(os.path.getsize('ex.json')/3)  # in bytes
# file_number = 1
# with open('ex.json', 'rb') as f:
#     chunk = f.read(CHUNK_SIZE)
#     while chunk:
#         with open('DividedFiles/ex_json_part' + str(file_number), 'wb') as chunk_file:
#             chunk_file.write(chunk)
#         file_number += 1
#         chunk = f.read(CHUNK_SIZE)


def divideFileToChunks(fileName, numberOfChunks):
    #the division could lead to a float , but we the file can read # bytes that are integers.
    CHUNK_SIZE = math.ceil(os.path.getsize(
        f"Server_files/{fileName}") / numberOfChunks)     # We take the cieling of the divison result and no the floor to avoid losing data

    chunkNO = 1
    with open(f"Server_files/{fileName}", "rb") as chosenFile:
        
        while (newChunk:= chosenFile.read(CHUNK_SIZE)) != b'': #if what we read is not empty then we assign what was read to newChunk
            if chunkNO > numberOfChunks:
                break
            with open(f"DividedFiles/{fileName.split('.')[0]}_chunk_{chunkNO}.{fileName.split('.')[1]}", "wb") as fileChunk:
                fileChunk.write(newChunk)
            chunkNO += 1


divideFileToChunks("app.txt", 10)
