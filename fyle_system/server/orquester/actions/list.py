from actions.base import Action
class List(Action):
    def execute(self,*args,**kwargs)->list:
        if kwargs["type"] == "files":
            try:
                return [str(self.index.data["users"][kwargs["user"]]).encode("utf-8")]
            except:
                return [b"This user does not have files"]
        elif kwargs["type"] == "hash":
            return [str(list(self.index.data["hashes"].keys())).encode("utf-8")]