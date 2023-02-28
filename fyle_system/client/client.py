import zmq
import json
import argparse
import base64
import hashlib


def open_file(file_name:str)->bytes:
    file = open(file_name,"rb")
    data = file.read()
    file.close()
    return data

def hash_file(data:bytes)->str:
    hash = hashlib.sha512(data).hexdigest()
    return hash

def send_message(connection,request:list):
    connection.send_multipart(request)
    response = connection.recv_multipart()
    return response

def download(*args,**kwargs):
    message = {
        "action":"download",
        "payload":{
        "user":kwargs["user"],
        "file":kwargs["file"]
    }}
    response = send_message(kwargs["connection"],[json.dumps(message).encode("utf-8")])
    file_to_write = open(kwargs["file"],"wb")
    clean_bytes = response[-1]
    file_to_write.write(clean_bytes)
    file_to_write.close()
    print(f'File {kwargs["file"]} downloaded')

def list(*arg,**kwargs):
    message = {
        "action":"list",
        "payload":{
        "type":"files",
        "user":kwargs["user"]
    }}
    
    response = send_message(kwargs["connection"],[json.dumps(message).encode("utf-8")])
    print(f"listing files {response}")

def upload(*args,**kwargs):
    message = {
        "action":"list",
        "payload":{
            "type":"hash"
        }
    }
    response = send_message(kwargs["connection"],[json.dumps(message).encode("utf-8")])
    files_in_server = response[0].decode("utf-8")
    file_to_upload = open_file(kwargs["file"])
    hash = hash_file(file_to_upload)
    if hash not in files_in_server:
        message ={
            "action":"upload",
            "payload":{
                "name":kwargs["file"],
                "user":kwargs["user"],
                "type":"file"
            }
        }
        print(send_message(kwargs["connection"],[json.dumps(message).encode("utf-8"),file_to_upload]))
    else:
        message ={
            "action":"upload",
            "payload":{
                "name":kwargs["file"],
                "user":kwargs["user"],
                "type":"reference",
                "hash":hash
            }
        }
        print("file uploaded")
        send_message(kwargs["connection"],[json.dumps(message).encode("utf-8")])

ACTIONS_MAP={
    "download":download,
    "list":list,
    "upload":upload
}

def read_args():
    parser = argparse.ArgumentParser(description='Client to upload files to the file server')
    parser.add_argument("--host",required=True,help="The host of the file server")
    parser.add_argument("--port",required=True,help="The port of the server to send data")
    parser.add_argument("--action",required=True,help="The action to realize")
    parser.add_argument("--file",required=True,help="The file to upload or download")
    parser.add_argument("--user",required=True,help="User to been identified")
    args = parser.parse_args()
    return args


def read_file(file_name:str):
    file = open(file_name,"rb")
    data_from_file = base64.b64encode(file.read()).decode("utf-8")
    file.close()
    return data_from_file

def build_payload(user:str,action:str,data_from_file:bytes,file_name:str,payload:dict)->str:
    request = {
    "action":action,
    "payload":payload
    }
    payload = json.dumps(request).encode("utf-8")
    return payload

def open_conection(host:str,port:int):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(f"tcp://{host}:{port}")
    return socket


if __name__ == "__main__":
    args = read_args()
    connection = open_conection(args.host,args.port)
    print(vars(args))
    action = ACTIONS_MAP[args.action](connection=connection,**vars(args))