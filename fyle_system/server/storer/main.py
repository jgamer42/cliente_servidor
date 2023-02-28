import zmq
import json
import argparse
from actions import ACTION_MAPS
def read_args():
    parser = argparse.ArgumentParser(description='Client to upload files to the file server')
    parser.add_argument("--port",required=True,help="The port of the server to send data")
    args = parser.parse_args()
    return args

def set_up_application(port:int)->zmq.sugar.socket.Socket:
    context:zmq.Context = zmq.Context()
    socket:zmq.sugar.socket.Socket = context.socket(zmq.REP)
    socket.bind(f"tcp://*:{port}")
    return socket

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
    socket:zmq.sugar.socket.Socket = set_up_application(args.port)
    print(f"Storer ready o recive files on {args.port}")
    main_loop(socket)