import hashlib
DEFAULT_CHUNK_SIZE = (1024*1024)*5 #5MB


def hash_file(data:bytes)->str:
    hash = hashlib.sha512(data).hexdigest()
    return hash

def read_file(file_name:str)->list:
    global DEFAULT_CHUNK_SIZE
    file = open(file_name,"rb")
    output = []
    data_from_file = file.read(DEFAULT_CHUNK_SIZE)
    data = data_from_file
    output.append(data_from_file)
    while data_from_file:
        try:
            data_from_file = file.read(DEFAULT_CHUNK_SIZE)
            if data_from_file != None or  data_from_file != "":
                output.append(data_from_file)
                aux = data_from_file
                data = data + aux
                if data_from_file == aux:
                    print("True")
                else:
                    print("False")
            else:
                break
        except:
            break
            
    file.close()
    return data,output

def write_file(file_name:str,data:bytes):
    file = open(file_name,"wb")
    file.write(data)
    file.close()