

import argparse

from actions import Upload,List,Download
from connections import open_conection


def read_args():
    parser = argparse.ArgumentParser(description='Client to upload files to the file server')
    parser.add_argument("--host",required=True,help="The host of the file server")
    parser.add_argument("--port",required=True,help="The port of the server to send data")
    parser.add_argument("--action",required=True,help="The action to realize")
    parser.add_argument("--file",required=True,help="The file to upload or download")
    parser.add_argument("--user",required=True,help="User to been identified")
    args = parser.parse_args()
    return args


ACTIONS_MAP={
    "download":Download(),
    "list":List(),
    "upload":Upload()
}

ROUTING_MAP = {
}

if __name__ == "__main__":
    args = read_args()
    connection = open_conection(args.host,args.port)
    ROUTING_MAP["ORQUESTER"] = connection
    action = ACTIONS_MAP[args.action].execute(connection_pool=ROUTING_MAP,**vars(args))