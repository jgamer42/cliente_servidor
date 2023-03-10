from actions.base import Action

import json
class Download(Action):
    
    def execute(self,*args,**kwargs)->list:
        hash,chunks = self.find_in_index(kwargs["user"],kwargs["file"])
        return [json.dumps({
            "chunks":chunks,
            "hash":hash
        }).encode("utf-8")]
    
    def find_in_index(self,user:str,file_name:str)->str:
        try:
            hash_from_file = self.index.data["files"][f'{user}-{file_name}'].split(".")[0]
        except:
            hash_from_file = self.index.data["files"][f'{user}-{file_name}']
        return hash_from_file,self.index.data["hashes"][hash_from_file]
