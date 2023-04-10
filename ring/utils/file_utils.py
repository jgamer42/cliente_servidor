from tqdm import tqdm
CHUNK_SIZE =  (1024*1024)*5 #5MB
def read_file(file_to_read:str):
    global CHUNK_SIZE
    print("Chunking the file")
    file = open(file_to_read,"rb")
    output = []
    data_from_file = file.read(CHUNK_SIZE)
    data = data_from_file
    output.append(data_from_file)
    while data_from_file:
        data_from_file = file.read(CHUNK_SIZE)
        if data_from_file != None or  data_from_file != "":
            output.append(data_from_file)
            aux = data_from_file
            data = data + aux
        else:
            break
    return data,output

def write_file(data,file_name):
    file = open(file_name,"wb")
    file.write(data)
    file.close()

def read_chunk(file_to_read):
    file = open(file_to_read,"rb")
    data = file.read()
    file.close()
    return data
