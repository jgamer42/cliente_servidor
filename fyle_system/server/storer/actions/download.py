class Download():
    def execute(self,*args,**kwargs)->list:
        file_to_open = kwargs["file"]
        file = open(f'carpeta_guardado/{file_to_open}',"rb")
        data_from_file = file.read()
        file.close()
        return [b"File Downloaded",data_from_file]