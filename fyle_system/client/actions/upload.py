import json
from file_handling import read_file,hash_file
from connections import open_conection

class Upload():
    def execute(self,file:str,connection_pool:dict,user:str,**kwargs)->dict:
        data,chunks = read_file(file)
        hash_from_file = hash_file(data)
        if not self.file_exist_in_server(hash_from_file,connection_pool["ORQUESTER"]):
            storers = self.get_storers(len(chunks),connection_pool["ORQUESTER"])
            stored_chunks = self.store_chunks(chunks,storers,connection_pool)
            self.notify_upload_file(user,file,hash_from_file,stored_chunks,connection_pool["ORQUESTER"])
        else:
            self.upload_reference(user,file,hash_from_file,connection_pool["ORQUESTER"])
    
    def file_exist_in_server(self,hash:str,connection:object)->bool:
        message = {
            "action":"list",
            "payload":{
                "type":"hash"
            }
        }
        connection.send_multipart([json.dumps(message).encode("utf-8")])
        response = connection.recv_multipart()
        files_in_server = response[0].decode("utf-8")
        return hash in files_in_server

    
    def upload_reference(self,user:str,user_file_name:str,hash_file:str,connection:object):
        message = {
            "action":"upload",
            "payload":{
                "type":"reference",
                "user":user,
                "name":user_file_name,
                "hash":hash_file
            }
        }
        connection.send_multipart([json.dumps(message).encode("utf-8")])
        response = connection.recv_multipart()
        print(response[0].decode("utf-8"))

    def notify_upload_file(self,user:str,file:str,hash_from_file:str,stored_chunks:list,connection:object):
        message = {
            "action":"upload",
            "payload":{
                "user":user,
                "name":file,
                "hash":hash_from_file,
                "chunks":stored_chunks,
                "type":"reference"
            }
        }
        connection.send_multipart([json.dumps(message).encode("utf-8")])
        response = connection.recv_multipart()
        print(response[0].decode("utf-8"))


    def get_storers(self,number_of_chunks:int,connection:dict)->list:
        message = {
            "action":"upload",
            "payload":{
                "type":"file",
                "chunks":number_of_chunks
            }
        }
        connection.send_multipart([json.dumps(message).encode("utf-8")])
        response = connection.recv_multipart()
        return json.loads(response[0].decode("utf-8"))

    def store_chunks(self,chunks,storers,connection_pool):
        part = 1
        used_storers = []
        i = 0
        message = {
            "action":"upload",
            "payload":{}
        }
        hasshes = []
        for chunk in chunks:
            if len(used_storers) == storers:
                used_storers = []
                i = 0
            else: 
                i += 1
            try:
                storer = storers[i]
                used_storers.append(storer)
            except IndexError:
                used_storers = []
                i = 0
                storer = storers[i]
                used_storers.append(storer)
            if storer in connection_pool.keys():
                connection = connection_pool[storer]
            else:
                host = storer.split(":")[0]
                port = storer.split(":")[1]
                connection = open_conection(host,port)
                connection_pool[storer] = connection
            connection.send_multipart([json.dumps(message).encode("utf-8"),chunk])
            response = connection.recv_multipart()
            stored_hash = response[0].decode("utf-8")
            hasshes.append({storer:stored_hash,"part":part})
            part += 1
        return hasshes
        
    
