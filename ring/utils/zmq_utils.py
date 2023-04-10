import zmq
from zmq.sugar.socket import Socket


def get_send_socket(context:zmq.Context,host:str)->Socket:
    sender:Socket = context.socket(zmq.REQ)
    sender.connect(f"tcp://{host}")
    return sender

def get_recieve_socket(context:zmq.Context,port:int)->Socket:
    receiver:Socket = context.socket(zmq.REP)
    receiver.bind(f"tcp://*:{port}")
    return receiver

def get_context():
    context:zmq.Context = zmq.Context()
    return context