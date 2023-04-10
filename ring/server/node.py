import os
import sys
from action_range import Range
from dotenv import load_dotenv
load_dotenv()
utils_path:str=os.getenv("PROJECT_UTILS","")
if utils_path:
    sys.path.append(utils_path)
else:
    print(".env not configured killing the server")
    sys.exit(1)

from zmq_utils import get_send_socket
from zmq import Context
from zmq.sugar.socket import Socket

class Node:
    def __init__(self,range:list,predecessor_host:str,context:Context):
        self.range:Range = Range(range[0],range[1])
        self.predecessor_host:str = predecessor_host
        self.context:Context = context
        self.predecessor_socket:Socket = get_send_socket(self.context,self.predecessor_host)
        self.handled_files = []
    
    def __len__(self):
        return len(self.range)
    
    def __contains__(self,id):
        return id in self.range
    
    def serialize(self):
        output = {
            "range":self.range.serialize(),
            "predecessor":self.predecessor_host
        }
        return output
    
    def update(self,new_id:int,new_predecessor:str):
        self.range.update(new_id)
        self.predecessor_socket.close()
        self.predecessor_host = new_predecessor
        self.predecessor_socket = get_send_socket(self.context,new_predecessor)
    
    def clean_file(self,file:str):
        self.handled_files.remove(file)
