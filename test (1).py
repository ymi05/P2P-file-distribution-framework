import os



#merge
mylist = os.listdir('.') 
mylist=list(filter(lambda k: k.startswith('my_song_'), mylist))
mylist.sort(key=lambda x: int(x[len('my_song_part_'):]))
print(mylist)

for file in mylist:
    with open('full_file','ab') as total_file:
        with open(file, 'rb') as chunk_file:
            for line in chunk_file:
                total_file.write(line)



#divide into chunks
CHUNK_SIZE = 8000000 # in bytes
file_number = 1
with open('01. Tempestuous Temperaments.mkv', 'rb') as f:
    chunk = f.read(CHUNK_SIZE)
    while chunk:
        with open('my_song_part_' + str(file_number), 'wb') as chunk_file:
            chunk_file.write(chunk)
        file_number += 1
        chunk = f.read(CHUNK_SIZE)

