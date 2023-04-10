import os
import sys
import json
from dotenv import load_dotenv
load_dotenv()
utils_path:str=os.getenv("PROJECT_UTILS","")
if utils_path:
    sys.path.append(utils_path)
else:
    print(".env not configured killing the server")
    sys.exit(1)
from file_utils import read_file,write_file
from utils import get_hash
from zmq_utils import get_send_socket

class Upload:
    def execute(self,context,file:str,host:str,output:str,*args,**kwargs):
        file_to_export = {"chunks":{}}
        data_file,chunks = read_file(file)
        file_hash = get_hash(data_file)
        file_to_export["hash"] = file_hash
        message = {
            "action":"upload",
            "payload":{
                "type":"ask"
            }
        }
        print("sending to store")
        for i,chunk in enumerate(chunks):
            chunk_hash = get_hash(chunk)
            message["payload"]["id"] = chunk_hash
            file_to_export["chunks"][i] = chunk_hash
            accepted = False
            node_to_ask = host
            while not accepted:
                socket = get_send_socket(context,node_to_ask)
                socket.send_multipart([json.dumps(message).encode("utf-8")])
                raw_response = socket.recv_multipart()
                response = json.loads(raw_response[0])
                accepted = response["acepted"]
                node_to_ask = response["host"]
                socket.close()
            new_message = {
                "action":"upload",
                "payload":{
                    "type":"accept",
                    "id":chunk_hash
                }
            }
            socket = get_send_socket(context,node_to_ask)
            socket.send_multipart([json.dumps(new_message).encode("utf-8"),chunk])
            raw_response = socket.recv_multipart()
            response = json.loads(raw_response[0])
        print("file stored")
        write_file(json.dumps(file_to_export).encode("utf-8"),output)