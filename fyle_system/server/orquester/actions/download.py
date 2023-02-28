from actions.base import Action
import io
import json
import hashlib

class Download(Action):
    
    def execute(self,*args,**kwargs)->list:
        hash,chunks = self.find_in_index(kwargs["user"],kwargs["file"])
        data = io.BytesIO()
        for chunk in chunks:
            print(chunk)
            message = {
                "action":"download",
                "payload":{
                    "file":chunk[list(chunk.keys())[0]]
                }
            }
            host_of_chunk = list(chunk.keys())[0]
            self.connections.data[host_of_chunk].send_multipart([json.dumps(message).encode("utf-8")])
            data_from_chunk = self.connections.data[host_of_chunk].recv_multipart()[0]
            print(data_from_chunk)
            data.write(data_from_chunk)
        output_data = data.read()
        validation_hash = self.get_file_name(output_data)
        if validation_hash == hash:
            return [b"file downloaded",output_data]
        else:
            return [b"the file is broken",b""]
        #file = open(f'carpeta_guardado/{file_to_open}',"rb")
        #data_from_file = file.read()
        #file.close()
        #return [b"File Downloaded",data_from_file]
    
    def find_in_index(self,user:str,file_name:str)->str:
        try:
            hash_from_file = self.index.data["files"][f'{user}-{file_name}'].split(".")[0]
        except:
            hash_from_file = self.index.data["files"][f'{user}-{file_name}']
        return hash_from_file,self.index.data["hashes"][hash_from_file]
    
    def get_file_name(self,data:bytes)->str:
        hash = hashlib.sha512(data).hexdigest()
        return hash