from actions.base import Action
import random
import json
DEFAULT_CHUNK_SIZE = (1024*1024)*5 #5MB
class Upload(Action):
    def execute(self,*args,**kwargs)->bytes:
        global DEFAULT_CHUNK_SIZE
        if kwargs["type"] == "file":
            number_of_chunks = kwargs["chunks"]
            output = self.pick_storers(number_of_chunks)
            return [json.dumps(output).encode("utf-8")]
        elif kwargs["type"] == "reference":
            self.save_in_index_map(kwargs["user"],kwargs["name"],kwargs.get("hash"),kwargs.get("chunks",None))
            return [f"File {kwargs['name']} succesfully uploaded".encode("utf-8")]
        
    
    def save_in_index_map(self,user:str,user_file_name:str,file_name:str=None,chunks:list=None)->None:
        if user in self.index.data["users"]:
            self.index.data["users"][user].append(user_file_name)
        else:
            self.index.data["users"][user] = [user_file_name]
        if chunks != None:
            self.index.data["hashes"][file_name] = chunks
        self.index.data["files"][f"{user}-{user_file_name}"] = f"{file_name}"
    

    def pick_storers(self,number_of_chunks:int):
        global DEFAULT_CHUNK_SIZE
        available_storers = len(list(self.config.data["storers"].keys()))
        number_of_storers = random.randint(2,available_storers)
        posible_storers = list(filter(lambda x: int(x[1]["size"]) > float(DEFAULT_CHUNK_SIZE),self.config.data["storers"].items()))
        choseen_storers = random.sample(posible_storers,k=number_of_storers)
        while (number_of_chunks * DEFAULT_CHUNK_SIZE) >  sum(storer[1]["size"] for storer in choseen_storers):
            number_of_storers = random.randint(2,available_storers)
            choseen_storers = random.sample(posible_storers,k=number_of_storers)
        return [choseen_storer[0] for choseen_storer in choseen_storers]

        