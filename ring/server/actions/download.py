import json
class Download:
    def execute(self,file:str,current_node,app,*args,**kwargs):
        if file in current_node.handled_files:
            message = {
                "stored":True,
                "chunk":file
            }
            data_file = app.find_file(file)
            return [json.dumps(message).encode("utf-8"),data_file]
        else:
            message = {
                "stored":False,
                "host":current_node.predecessor_host
            }
            return [json.dumps(message).encode("utf-8")]