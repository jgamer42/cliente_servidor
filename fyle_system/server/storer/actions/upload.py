import hashlib

class Upload():
    def execute(self,*args,**kwargs):
        file_name = self.get_file_name(kwargs["data"])
        self.write_file(file_name,kwargs["data"])
        return [f"{file_name}".encode("utf-8")]
    
    def get_file_name(self,data:bytes)->str:
        hash = hashlib.sha512(data).hexdigest()
        return hash

    def write_file(self,file_name:str,data:bytes)->None:
        file_to_write = open(f'carpeta_guardado/{file_name}',"wb")
        file_to_write.write(data)
        file_to_write.close()
        