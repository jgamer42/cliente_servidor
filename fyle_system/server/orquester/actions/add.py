from actions.base import Action
class Add(Action):
    def execute(self, *args, **kwargs):
        try:
            host = kwargs["host"]
            port = kwargs["port"]
            size = kwargs["size"]
            path = f"{host}:{port}"
            storer_to_add ={
                "files":[],
                "size":size
            }
            if path in self.config.data["storers"].keys():
                return["rejected".encode("utf-8")]
            self.config.data["storers"][path] = storer_to_add 
            return ["accepted".encode("utf-8")]
        except:
            return ["rejected".encode("utf-8")]