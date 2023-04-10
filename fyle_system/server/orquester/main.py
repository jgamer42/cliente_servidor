import zmq
import json
from actions import ACTION_MAPS
from helpers import Index,Config
from actions.base import Action

def set_up_application(port:int)->zmq.sugar.socket.Socket:
    context:zmq.Context = zmq.Context()
    socket:zmq.sugar.socket.Socket = context.socket(zmq.REP)
    socket.bind(f"tcp://*:{port}")
    print(type(socket))
    return socket

def main_loop(socket:zmq.Context)->None:
    while True:
        raw_message:bytes = socket.recv_multipart()
        print(f"Message received {raw_message}")
        pre_prod_message:str = raw_message[0].decode("utf-8")
        file = raw_message[1] if len(raw_message) > 1 else None
        payload:dict = json.loads(pre_prod_message)
        
        action_to_execute:Action = ACTION_MAPS[payload["action"]]
        response:list = action_to_execute.execute(**payload["payload"],data=file)
        print(f"Message answered {response[0]}")
        socket.send_multipart(response)

if __name__ == '__main__':
    index:Index = Index()
    config:Config = Config()
    socket:zmq.sugar.socket.Socket = set_up_application(config.data["port"])
    try:
        print("API ready to recive messages")
        main_loop(socket)
    finally:
        print("Exporting the index data")
        index.export()
        config.export()
        print("Succesfully exported")