
import os
import sys
import json
from argparse import  Namespace
from dotenv import load_dotenv
from zmq.sugar.socket import Socket
from zmq import Context
from actions import AddNode,Upload,Download
from node import Node
import logging
load_dotenv()
utils_path:str=os.getenv("PROJECT_UTILS","")
if utils_path:
    sys.path.append(utils_path)
else:
    print(".env not configured killing the server")
    sys.exit(1)
from zmq_utils import get_recieve_socket,get_context,get_send_socket
from file_utils import write_file,read_chunk

class App:
    def __init__(self,id:int,config:Namespace):
        self.actions:dict = {
            "add_node":AddNode(),
            "upload":Upload(),
            "download":Download()
        }
        self.host:str = f"{config.host}:{config.port}"
        self.name:str = config.name
        self.context:Context = get_context()
        self.id:int = id
        self.receiver_socket:Socket = get_recieve_socket(self.context,config.port)
        self.folder:str = config.name
        self.create_folder()
        if config.first:
            self.node = Node([0,pow(2,512)-1],self.host,self.context)
        else:
            message = {
                "action":"add_node",
                "payload":{
                    "id":self.id,
                    "host":self.host
                }
            }
            accepted = False
            host_to_ask = config.predecessor
            while not accepted:
                node_to_ask = get_send_socket(self.context,host_to_ask)
                node_to_ask.send_multipart([json.dumps(message).encode("utf-8")])
                raw_response = node_to_ask.recv_multipart()
                response = json.loads(raw_response[0].decode("utf-8"))
                accepted = response["acepted"]
                if accepted:
                    self.node = Node([response["id"]+1,self.id],response["host"],self.context)
                    if response["has_files"]:
                        for pos,file in enumerate(raw_response[1:]):
                            id = response["files"][pos]
                            write_file(file,f"{self.folder}/{id}")
                else:
                    host_to_ask = response["host"]

    def export(self):
        output = open(f"{self.name}.json","w+")
        data = self.node.serialize()
        data["host"] = self.host
        data = json.dumps(data)
        output.write(data)
        output.close()
    
    def clean_file(self,file:str):
        existent_files = os.listdir(self.folder)
        if file in existent_files:
            os.remove(f"{self.folder}/{file}")
    
    def create_folder(self):
        if not (os.path.exists(self.folder) and os.path.isdir(self.folder)):
            os.makedirs(self.folder)

    def find_file(self,file):
        data = read_chunk(f"{self.folder}/{file}")
        return data
    
    def main_loop(self):
        while True:
            message:list = self.receiver_socket.recv_multipart()
            logging.debug(f"llego {message[0]}")
            payload:dict = json.loads(message[0].decode("utf-8"))
            action:str = payload["action"]
            action_payload:dict = payload["payload"]
            try:
                response:list = self.actions[action].execute(current_node=self.node,app_id=self.id,app=self,file=message[1],**action_payload)
            except IndexError:
                response:list = self.actions[action].execute(current_node=self.node,app_id=self.id,app=self,**action_payload)
            self.receiver_socket.send_multipart(response)
            logging.debug(f"respondi {response[0]}")
