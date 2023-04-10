import os
import sys
from argparse import  ArgumentParser,Namespace
from dotenv import load_dotenv
load_dotenv()
utils_path:str=os.getenv("PROJECT_UTILS","")
if utils_path:
    sys.path.append(utils_path)
else:
    print(".env not configured killing the server")
    sys.exit(1)
from actions import Upload
from zmq_utils import get_context

ACTIONS_MAPS={
    "upload":Upload()
}
def read_args()->Namespace:
    parser:ArgumentParser = ArgumentParser(description='Client to upload files to the file server')
    parser.add_argument("--host",required=True,help="The host to send the file")
    parser.add_argument("--action",required=True)
    parser.add_argument("--file",required=True)
    parser.add_argument("--output",required=True)
    return vars(parser.parse_args())


if __name__ == '__main__':
    args = read_args()
    zmq_context = get_context()
    ACTIONS_MAPS[args["action"]].execute(context=zmq_context,**args)