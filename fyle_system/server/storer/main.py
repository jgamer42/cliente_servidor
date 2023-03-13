import zmq
import json
import argparse
from actions import ACTION_MAPS
import json
import sys
import random
SIZE = (1024*1024)*random.randint(100,500)
def read_args():
    parser = argparse.ArgumentParser(description='Client to upload files to the file server')
    parser.add_argument("--host",required=True,help="The host or the IP where the storer is set up")
    parser.add_argument("--port",required=True,help="The port of the server to send data")
    args = parser.parse_args()
    return args

def set_up_application(host:str,port:int,orquester:str)->zmq.sugar.socket.Socket:
    context:zmq.Context = zmq.Context()
    register_in_system(host,port,context,orquester)
    receiver:zmq.sugar.socket.Socket = context.socket(zmq.REP)
    receiver.bind(f"tcp://*:{port}")
    return receiver

def register_in_system(host,port,context,orquester)->None:
    global SIZE
    message = {
        "action":"add",
        "payload":{
            "host":host,
            "port":port,
            "size":SIZE
        }
    }
    sender:zmq.sugar.socket.Socket = context.socket(zmq.REQ)
    sender.connect(f"tcp://{orquester}")
    sender.send_multipart([json.dumps(message).encode("utf-8")])
    response = sender.recv_multipart()[0].decode('utf-8')
    if response == "accepted":
        print(f"status {response} from the orquester")
    else:
        print("Storer rejected from the orquester try again")
        sys.exit()
def main_loop(socket:zmq.Context)->None:
    while True:
        raw_message:bytes = socket.recv_multipart()
        pre_prod_message:str = raw_message[0].decode("utf-8")
        file = raw_message[1] if len(raw_message) > 1 else None
        payload:dict = json.loads(pre_prod_message)
        action_to_execute = ACTION_MAPS[payload["action"]]
        response:list = action_to_execute.execute(**payload["payload"],data=file)
        socket.send_multipart(response)

if __name__ == '__main__':
    args = read_args()
    config_file = open("config.json","r")
    config = json.load(config_file)
    config_file.close()
    socket:zmq.sugar.socket.Socket = set_up_application(args.host,args.port,config["orquester"])
    print(f"Storer ready o recive files on {args.port}")
    main_loop(socket)