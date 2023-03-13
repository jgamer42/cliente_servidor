import json
import io
from file_handling import hash_file,write_file
from connections import open_conection

class Download():
    def execute(self,file:str,connection_pool:dict,user:str,**kwargs):
        file_information = self.get_storers_from_file(file,user,connection_pool["ORQUESTER"])
        data = self.download_from_storers(file_information["chunks"],connection_pool)
        hash = hash_file(data)
        if hash == file_information["hash"]:
            write_file(file,data)
            print(f"File {file} downloaded")
        else:
            print("File corrupted")
        
    
    def get_storers_from_file(self,file,user,connection)->dict:
        message = {
            "action":"download",
            "payload":{
                "file":file,
                "user":user
            }
        }
        connection.send_multipart([json.dumps(message).encode("utf-8")])
        response = connection.recv_multipart()
        file_data = json.loads(response[0].decode("utf-8"))
        return file_data
    
    def download_from_storers(self,chunks,connection_pool):
        data = io.BytesIO()
        for chunk in chunks:
            message = {
                "action":"download",
                "payload":{
                    "file":chunk[list(chunk.keys())[0]]
                }
            }
            storer = list(chunk.keys())[0]

            if storer in connection_pool.keys():
                connection = connection_pool[storer]
            else:
                host = storer.split(":")[0]
                port = storer.split(":")[1]
                connection = open_conection(host,port)
                connection_pool[storer] = connection
            connection.send_multipart([json.dumps(message).encode("utf-8")])
            data_from_chunk = connection.recv_multipart()[1]
            data.write(data_from_chunk)
        return data.getvalue()