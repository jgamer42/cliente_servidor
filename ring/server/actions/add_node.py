
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
from utils import binary_search_with_position
from file_utils import read_chunk
class AddNode:
    def execute(self,id:int,host:str,current_node,app,*args,**kwargs)->list:
        clean_id =id
        if clean_id in current_node:
            response = {
                "acepted":True,
                "host":current_node.predecessor_host,
                "id":app.id,
                "has_files":False
            }
            current_node.update(clean_id,host)
            files_to_find = sorted(current_node.handled_files,key=lambda x: int(x,16))
            limit_file = binary_search_with_position(files_to_find,hex(id))
            transfer_files = []
            if limit_file[0] == limit_file[1]:
                transfer_files = files_to_find[:limit_file[0]]
            elif int(files_to_find[limit_file[1]],16) <= clean_id:
                transfer_files = files_to_find[:limit_file[1]] 
            elif int(files_to_find[limit_file[1]],16) >= clean_id:
                transfer_files = files_to_find[:limit_file[1]-1]
            if len(transfer_files) != 0:
                response["has_files"] = True
                files_data =[]
                for file in transfer_files:
                    data = read_chunk(f"{app.folder}/{file}")
                    current_node.clean_file(file)
                    app.clean_file(file)
                    files_data.append(data)
                response["files"] = transfer_files
                return [json.dumps(response).encode("utf-8"),*files_data]
            return [json.dumps(response).encode("utf-8")]
        else:
            response = {
                "acepted":False,
                "host":current_node.predecessor_host
            }
            return [json.dumps(response).encode("utf-8")]