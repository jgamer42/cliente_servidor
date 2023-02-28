import hashlib
from actions.base import Action
import sys
import random
import io
import json

class Upload(Action):
    mb = 1024*1024
    def execute(self,*args,**kwargs)->bytes:
        try:
            self.extension = kwargs["name"].split(".")[-1]
        except:
            self.extension = ""
        if kwargs["type"] == "file":
            file_name = self.get_file_name(kwargs["data"])
            chunks = self.send_to_storers(kwargs["data"])
            self.save_in_index_map(kwargs["user"],kwargs["name"],file_name,chunks)
            return [f"File {kwargs['name']} succesfully uploaded".encode("utf-8")]
        elif kwargs["type"] == "reference":
            file_name = kwargs["hash"]
            self.save_in_index_map(kwargs["user"],kwargs["name"],file_name,[])
            return [f"File {kwargs['name']} succesfully uploaded".encode("utf-8")]
        
    def get_file_name(self,data:bytes)->str:
        hash = hashlib.sha512(data).hexdigest()
        return hash
    
    def save_in_index_map(self,user:str,user_file_name:str,file_name:str,chunks:list)->None:
        if user in self.index.data["users"]:
            self.index.data["users"][user].append(user_file_name)
        else:
            self.index.data["users"][user] = [user_file_name]
        if file_name not in self.index.data["hashes"].keys():
            self.index.data["hashes"][file_name] = chunks
        self.index.data["files"][f"{user}-{user_file_name}"] = f"{file_name}.{self.extension}"
    
    def send_to_storers(self,data:bytes)->None:
        chunks_stored = []
        processed_data = io.BytesIO(data)
        size_of_data = sys.getsizeof(data)/self.mb
        number_of_chunks,size_of_chunk = self.load_balancing(size_of_data)
        storers = self.pick_storers(number_of_chunks,size_of_chunk)
        chunks = self.split_the_file(size_of_chunk,processed_data,number_of_chunks)
        message = {
            "action":"upload",
            "payload":{}
        }
        #not have carry_over
        if len(chunks) == len(storers):
            pass
        else:
            storers = storers + [storers[-1] * (len(chunks)-len(storers))]
        for i,chunk in enumerate(chunks):
            target_storer = storers[i-1] 
            self.connections.data[target_storer].send_multipart([json.dumps(message).encode("utf-8"),chunk])
            hassh_stored = self.connections.data[target_storer].recv_multipart()[0].decode("utf-8")
            chunk_stored ={
                target_storer:hassh_stored
            }
            chunks_stored.append(chunk_stored)
        return chunks_stored
    
    def split_the_file(self,size_of_chunk:int,file:bytes,number_of_chunks:int):
        output = []
        for _ in range(number_of_chunks):
            data = file.read(size_of_chunk*self.mb)
            output.append(data)
        try:
            output.append(file.read(size_of_chunk*self.mb))
        except:
            pass
        return output
    
    def load_balancing(self,file_syze:int):
        available_storers = len(list(self.config.data["storers"].keys()))
        storers_to_use = random.randint(2,available_storers)
        size_of_chunk = int(file_syze//storers_to_use)
        return storers_to_use,size_of_chunk
    
    def pick_storers(self,n_storers:int,size_of_chunk:int):
        print(n_storers,size_of_chunk)
        posible_storers = list(filter(lambda x: int(x[1]["size"]) > float(1.5*size_of_chunk),self.config.data["storers"].items()))
        print(posible_storers)
        return random.sample([storer[0] for storer in posible_storers],k=n_storers)
        