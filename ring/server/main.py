import os
import sys
import uuid
from argparse import  ArgumentParser,Namespace,_MutuallyExclusiveGroup
from app import App
from dotenv import load_dotenv
load_dotenv()
utils_path:str=os.getenv("PROJECT_UTILS","")
if utils_path:
    sys.path.append(utils_path)
else:
    print(".env not configured killing the server")
    sys.exit(1)

from utils import get_hash



def read_args()->Namespace:
    parser:ArgumentParser = ArgumentParser(description='Client to upload files to the file server')
    constraints:_MutuallyExclusiveGroup = parser.add_mutually_exclusive_group()
    parser.add_argument("--host",required=True,help="The host or the IP where the storer is set up")
    parser.add_argument("--name",required=True,help="The host or the IP where the storer is set up")
    parser.add_argument("--port",required=True,help="The port of the server to send data")
    constraints.add_argument("--first",required=False,help="Flag used to start a new ring",nargs="?",const=True,type=bool,default=False)
    constraints.add_argument("--predecessor",required=False,help="Preivous node that you kwon")
    return parser.parse_args()

def set_up_app(args:Namespace)->App:
    node_id:bytes = str(uuid.uuid4()).encode("utf-8")
    node_id:str = get_hash(node_id)
    node_id:int = int(node_id,16)
    return App(node_id,args) 


if __name__ == "__main__":
    args:Namespace = read_args()
    app:App = set_up_app(args)
    print("App receiving messages")
    try:
        app.main_loop()
    except KeyboardInterrupt:
        #app.export()
        print("sali")
