import json
import os
import sys
from dotenv import load_dotenv
load_dotenv()
utils_path:str=os.getenv("PROJECT_UTILS","")
if utils_path:
    sys.path.append(utils_path)
else:
    print(".env not configured killing the server")
    sys.exit(1)
from file_utils import write_file
class Upload:
    def execute(self,id:str,type:str,current_node,app,file=None,*args,**kwargs)->list:
        subaction = getattr(self,type)
        response = subaction(id=id,current_node=current_node,file=file,app=app)
        return [json.dumps(response).encode("utf-8")]

    def ask(self,id,current_node,app,*args,**kwargs):
        file_id = int(id,16)
        if file_id in current_node:
            response = {
                    "acepted":True,
                    "host":app.host
                }
        else:
             response = {
                    "acepted":False,
                    "host":current_node.predecessor_host
                }
        return response

    def accept(self,id,file,app,current_node,*args,**kwargs):
        write_file(file,f"{app.folder}/{id}")
        response = {
            "recieved":True
        }
        current_node.handled_files.append(id)
        return response